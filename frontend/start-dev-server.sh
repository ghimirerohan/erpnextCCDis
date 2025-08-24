#!/bin/bash

# Start Vue.js development server for mobile access
echo "Starting Vue.js development server..."
echo "Server will be accessible at:"
echo "  - Local: http://localhost:8080"
echo "  - Network: http://192.168.1.75:8080 (if port forwarding is configured)"
echo ""
echo "To access from your mobile device:"
echo "1. Make sure port 8080 is forwarded from Docker container to host"
echo "2. Access: http://192.168.1.75:8080"
echo ""

# Start the development server
npm run dev
