# Mobile Access Guide for Vue.js Sales Invoice Dashboard

## 🎯 Problem
Your Vue.js frontend is running on port 8080 but not accessible from your mobile device at `192.168.1.75:8080`.

## 🔧 Solution

### Option 1: Docker Port Forwarding (Recommended)

If you're running this in Docker, you need to map port 8080 from the container to your host machine.

#### For Docker Compose:
Add this to your `docker-compose.yml`:
```yaml
services:
  your-service-name:
    # ... other config
    ports:
      - "8080:8080"  # Map container port 8080 to host port 8080
```

#### For Docker Run:
```bash
docker run -p 8080:8080 your-image-name
```

### Option 2: Direct Host Access

If you want to run the Vue.js app directly on your host machine:

1. **Copy the frontend to your host machine:**
```bash
# From your host machine (not inside Docker)
cp -r /path/to/frappe-bench/apps/custom_erp/frontend ~/vue-sales-dashboard
cd ~/vue-sales-dashboard
npm install
```

2. **Start the development server:**
```bash
npm run dev
```

### Option 3: Build and Serve Static Files

1. **Build the Vue.js app:**
```bash
cd apps/custom_erp/frontend
npm run build
```

2. **Serve the built files:**
```bash
# Install a simple HTTP server
npm install -g serve

# Serve the built files
serve -s dist -l 8080
```

## 🌐 Access URLs

Once configured, you can access the app at:
- **Local (same machine):** `http://localhost:8080`
- **Mobile/Network:** `http://192.168.1.75:8080`

## 🔍 Troubleshooting

### Check if server is running:
```bash
# Inside the container
netstat -tlnp | grep 8080
```

### Check if port is accessible:
```bash
# From your host machine
curl -I http://localhost:8080
```

### Check Docker port mapping:
```bash
docker ps
# Look for the port mapping in the output
```

## 📱 Mobile Testing

1. **Ensure your mobile is on the same WiFi network**
2. **Open browser on mobile**
3. **Navigate to:** `http://192.168.1.75:8080`
4. **Test the searchable customer dropdown and all features**

## 🚀 Quick Start (Current Setup)

The Vue.js server is already configured to:
- ✅ Run on port 8080
- ✅ Bind to all interfaces (0.0.0.0)
- ✅ Allow connections from 192.168.1.75
- ✅ Support Hot Module Replacement (HMR)

**You just need to ensure port 8080 is forwarded from Docker container to your host machine.**

## 🔧 Current Configuration

The `vite.config.js` is already configured with:
```javascript
server: {
  host: '0.0.0.0',
  port: 8080,
  allowedHosts: ['192.168.1.75', 'localhost', '127.0.0.1'],
  hmr: {
    host: '192.168.1.75',
    port: 8080
  }
}
```

## 📞 Next Steps

1. **Configure Docker port forwarding** (if using Docker)
2. **Test access from mobile** at `http://192.168.1.75:8080`
3. **Enjoy the searchable customer dropdown and sales invoice dashboard!**

---

**Note:** The Vue.js app includes all the features you requested:
- ✅ Searchable customer dropdown
- ✅ Date range filters
- ✅ Bill-wise and Summary views
- ✅ Responsive design for mobile
- ✅ Real-time data from ERPNext
