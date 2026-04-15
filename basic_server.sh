#!/bin/bash

# Basic TLS Server - Only show encrypted/decrypted messages

echo "================================================================================"
echo "  🔐 TLS SERVER"
echo "================================================================================"
echo ""
echo "  Listening on port 4433..."
echo ""
echo "================================================================================"
echo ""

CONNECTION_NUM=0

while true; do
    CONNECTION_NUM=$((CONNECTION_NUM + 1))
    
    echo ""
    echo "================================================================================"
    echo "CONNECTION #$CONNECTION_NUM - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "================================================================================"
    echo ""
    
    # Start server and capture output
    openssl s_server \
        -accept 4433 \
        -cert certs/server.crt \
        -key certs/server.key \
        -quiet \
        2>&1 | while IFS= read -r line; do
        
        if [ ! -z "$line" ]; then
            echo "📦 ENCRYPTED MESSAGE: [Binary TLS encrypted data]"
            echo "🔓 DECRYPTED MESSAGE: $line"
            echo ""
        fi
    done
    
    echo "Connection closed"
    echo ""
    
    sleep 0.5
done
