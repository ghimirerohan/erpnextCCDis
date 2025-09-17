"""
Memory optimization configuration for purchase invoice processing.
This module provides settings and utilities to prevent memory issues in production.
"""

import frappe
import gc
import psutil
import os
from typing import Dict, Any, Optional

class MemoryConfig:
    """Configuration class for memory optimization settings."""
    
    def __init__(self):
        self.settings = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load memory optimization settings from site config."""
        default_settings = {
            "enable_gc": True,
            "gc_threshold": 0.8,  # 80% memory usage threshold
            "max_memory_mb": 2048,  # 2GB max memory
            "batch_size": 50,  # Items per batch
            "cleanup_interval": 300,  # 5 minutes
            "force_cleanup_threshold": 0.9,  # 90% threshold for forced cleanup
        }
        
        try:
            site_settings = frappe.get_conf().get("memory_optimization", {})
            default_settings.update(site_settings)
        except Exception:
            pass
        
        return default_settings
    
    def check_memory_usage(self) -> Dict[str, Any]:
        """Check current memory usage and return status."""
        try:
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            
            # Get system memory info
            system_memory = psutil.virtual_memory()
            
            current_mb = memory_info.rss / 1024 / 1024
            system_total_mb = system_memory.total / 1024 / 1024
            system_used_mb = system_memory.used / 1024 / 1024
            
            usage_percent = (current_mb / self.settings["max_memory_mb"]) * 100
            system_usage_percent = (system_used_mb / system_total_mb) * 100
            
            return {
                "current_mb": round(current_mb, 2),
                "max_mb": self.settings["max_memory_mb"],
                "usage_percent": round(usage_percent, 2),
                "system_usage_percent": round(system_usage_percent, 2),
                "needs_cleanup": usage_percent > (self.settings["gc_threshold"] * 100),
                "needs_forced_cleanup": usage_percent > (self.settings["force_cleanup_threshold"] * 100),
                "system_critical": system_usage_percent > 95
            }
        except Exception as e:
            frappe.log_error(f"Memory check failed: {str(e)}", "Memory Check Error")
            return {
                "current_mb": 0,
                "max_mb": self.settings["max_memory_mb"],
                "usage_percent": 0,
                "system_usage_percent": 0,
                "needs_cleanup": False,
                "needs_forced_cleanup": False,
                "system_critical": False,
                "error": str(e)
            }
    
    def force_cleanup(self) -> bool:
        """Force garbage collection and memory cleanup."""
        try:
            if self.settings["enable_gc"]:
                # Force multiple garbage collection cycles
                for _ in range(3):
                    gc.collect()
                
                # Clear Frappe cache if available
                try:
                    frappe.clear_cache()
                except Exception:
                    pass
                
                # Clear any cached data
                try:
                    frappe.db.commit()
                except Exception:
                    pass
                
                return True
        except Exception as e:
            frappe.log_error(f"Memory cleanup failed: {str(e)}", "Memory Cleanup Error")
            return False
        
        return False
    
    def should_abort_operation(self) -> bool:
        """Check if current operation should be aborted due to memory constraints."""
        memory_status = self.check_memory_usage()
        
        # Abort if system memory is critically low
        if memory_status.get("system_critical", False):
            return True
        
        # Abort if our process is using too much memory
        if memory_status.get("needs_forced_cleanup", False):
            return True
        
        return False
    
    def get_batch_size(self) -> int:
        """Get optimal batch size based on memory usage."""
        memory_status = self.check_memory_usage()
        
        if memory_status.get("needs_cleanup", False):
            return max(10, self.settings["batch_size"] // 2)
        
        return self.settings["batch_size"]

# Global memory config instance
memory_config = MemoryConfig()

def get_memory_config() -> MemoryConfig:
    """Get the global memory configuration instance."""
    return memory_config

def log_memory_usage(operation: str, additional_info: Optional[Dict[str, Any]] = None):
    """Log memory usage for monitoring purposes."""
    try:
        memory_status = memory_config.check_memory_usage()
        log_data = {
            "operation": operation,
            "memory_usage_mb": memory_status["current_mb"],
            "memory_usage_percent": memory_status["usage_percent"],
            "system_usage_percent": memory_status["system_usage_percent"],
            "needs_cleanup": memory_status["needs_cleanup"],
            "timestamp": frappe.utils.now()
        }
        
        if additional_info:
            log_data.update(additional_info)
        
        # Log to Frappe error log for monitoring
        if memory_status["needs_cleanup"]:
            frappe.log_error(
                f"High memory usage detected: {log_data}",
                f"Memory Usage - {operation}"
            )
        
        # Also log to console in development
        if frappe.get_conf().get("developer_mode"):
            print(f"Memory Usage [{operation}]: {memory_status['current_mb']:.2f}MB ({memory_status['usage_percent']:.1f}%)")
            
    except Exception as e:
        frappe.log_error(f"Memory logging failed: {str(e)}", "Memory Logging Error")
