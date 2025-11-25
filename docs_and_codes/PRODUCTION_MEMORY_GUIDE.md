# Production Memory Optimization Guide

This guide provides comprehensive instructions to prevent memory issues when deploying the Custom ERP application in production, specifically for the purchase invoice creation functionality.

## Problem Summary

The application was experiencing Out of Memory (OOM) kills during purchase invoice creation due to:
- High memory usage during image processing
- Inefficient object creation and garbage collection
- System memory pressure from multiple processes
- Large payload processing without memory monitoring

## Solutions Implemented

### 1. Backend Memory Optimizations

#### API Level Optimizations
- **Garbage Collection**: Forced garbage collection at strategic points
- **Batch Processing**: Items processed in configurable batches (default: 50)
- **Memory Monitoring**: Real-time memory usage tracking with psutil
- **Early Abort**: Operations aborted when memory pressure is detected
- **Efficient Data Structures**: Reduced object creation and memory footprint

#### Key Files Modified:
- `custom_erp/custom_erp/purchase_invoice/api.py`
- `custom_erp/custom_erp/purchase_invoice/memory_config.py`

### 2. Frontend Memory Optimizations

#### Vue.js Optimizations
- **Memory Monitoring**: Browser memory usage tracking
- **Image Cleanup**: Proper URL.revokeObjectURL() calls
- **Efficient Data Processing**: Reduced object creation in loops
- **Memory Cleanup**: Automatic cleanup after operations

#### Key Files Modified:
- `frontend/src/pages/Scanner.vue`

### 3. System Configuration

#### Site Configuration
```json
{
  "memory_optimization": {
    "enable_gc": true,
    "gc_threshold": 0.8,
    "max_memory_mb": 2048,
    "batch_size": 50,
    "cleanup_interval": 300,
    "force_cleanup_threshold": 0.9
  }
}
```

## Production Deployment Steps

### 1. System Requirements

#### Minimum System Specifications
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: 2 cores minimum, 4 cores recommended
- **Storage**: 20GB available space
- **Swap**: 2GB swap space configured

#### Memory Configuration
```bash
# Add to /etc/sysctl.conf
vm.swappiness = 10
vm.vfs_cache_pressure = 50
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
```

### 2. Frappe Bench Configuration

#### Worker Configuration
```bash
# In Procfile
web: bench serve --port 8000 --noreload
worker: bench worker --queue default
schedule: bench schedule
socketio: /home/frappe/.nvm/versions/node/v20.19.2/bin/node apps/frappe/socketio.js
watch: bash -lc 'while true; do bench watch || true; sleep 1; done'
```

#### Gunicorn Configuration
```python
# In gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "gthread"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 120
keepalive = 2
preload_app = True
```

### 3. Database Optimization

#### MySQL/MariaDB Configuration
```ini
[mysqld]
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 2
innodb_flush_method = O_DIRECT
query_cache_size = 128M
query_cache_type = 1
max_connections = 200
```

### 4. Redis Configuration

#### Redis Memory Settings
```conf
# In redis.conf
maxmemory 512mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

### 5. Nginx Configuration

#### Nginx Memory Settings
```nginx
# In nginx.conf
worker_processes auto;
worker_rlimit_nofile 65536;
worker_connections 1024;

# Buffer sizes
client_body_buffer_size 128k;
client_max_body_size 10m;
client_header_buffer_size 1k;
large_client_header_buffers 4 4k;
```

### 6. Monitoring Setup

#### Memory Monitoring Script
```bash
#!/bin/bash
# monitor_memory.sh

while true; do
    MEMORY_USAGE=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2}')
    SWAP_USAGE=$(free -m | awk 'NR==3{printf "%.2f%%", $3*100/$2}')
    
    echo "$(date): Memory: $MEMORY_USAGE, Swap: $SWAP_USAGE"
    
    # Alert if memory usage is high
    if (( $(echo "$MEMORY_USAGE > 85" | bc -l) )); then
        echo "WARNING: High memory usage detected!"
        # Send alert (email, Slack, etc.)
    fi
    
    sleep 60
done
```

#### Log Rotation
```bash
# In /etc/logrotate.d/frappe
/workspace/frappe-bench/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 frappe frappe
    postrotate
        systemctl reload frappe-bench
    endscript
}
```

### 7. Application-Level Monitoring

#### Memory Usage Alerts
The application now includes built-in memory monitoring that:
- Logs memory usage at key points
- Aborts operations when memory pressure is detected
- Provides detailed memory usage reports
- Automatically cleans up memory when needed

#### Monitoring Endpoints
```python
# Available monitoring endpoints
GET /api/method/custom_erp.custom_erp.purchase_invoice.api.get_memory_status
POST /api/method/custom_erp.custom_erp.purchase_invoice.api.force_cleanup
```

### 8. Performance Testing

#### Load Testing
```bash
# Test purchase invoice creation under load
ab -n 100 -c 10 -p payload.json -T application/json http://localhost:8000/api/method/custom_erp.custom_erp.purchase_invoice.api.create_purchase_invoice
```

#### Memory Testing
```bash
# Monitor memory during operations
watch -n 1 'free -m && echo "---" && ps aux | grep frappe | head -5'
```

## Troubleshooting

### Common Issues

#### 1. OOM Kills Still Occurring
**Symptoms**: System kills Frappe processes
**Solutions**:
- Increase system RAM
- Reduce worker processes
- Implement memory limits
- Add swap space

#### 2. Slow Performance
**Symptoms**: Purchase invoice creation takes too long
**Solutions**:
- Optimize database queries
- Increase worker processes
- Enable caching
- Monitor and optimize memory usage

#### 3. Memory Leaks
**Symptoms**: Memory usage continuously increases
**Solutions**:
- Check for circular references
- Implement proper cleanup
- Monitor garbage collection
- Restart workers periodically

### Debugging Commands

```bash
# Check memory usage
free -h
ps aux | grep frappe

# Check logs
tail -f /workspace/frappe-bench/logs/frappe.log
tail -f /workspace/frappe-bench/logs/worker.log

# Check system resources
htop
iotop
```

## Best Practices

### 1. Regular Maintenance
- Monitor memory usage daily
- Restart workers weekly
- Clean up old logs monthly
- Update system packages regularly

### 2. Scaling Considerations
- Use load balancers for multiple instances
- Implement horizontal scaling
- Use CDN for static assets
- Consider microservices architecture

### 3. Backup and Recovery
- Regular database backups
- Configuration backups
- Disaster recovery plan
- Test recovery procedures

## Conclusion

These optimizations should prevent memory issues in production. The key is:
1. **Proactive Monitoring**: Always monitor memory usage
2. **Efficient Processing**: Use batch processing and cleanup
3. **System Optimization**: Configure system resources properly
4. **Regular Maintenance**: Keep the system healthy

For additional support, check the logs and monitor the memory usage patterns to identify any remaining issues.
