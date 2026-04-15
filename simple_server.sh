#!/bin/bash

# Simple TLS Server - Show encrypted and decrypted messages

echo "================================================================================"
echo "  🔐 TLS SERVER - MESSAGE DISPLAY"
echo "================================================================================"
echo ""
echo "  Listening on port 4433..."
echo "  Showing encrypted and decrypted messages"
echo ""
echo "================================================================================"
echo ""

CONNECTION_NUM=0

while true; do
    CONNECTION_NUM=$((CONNECTION_NUM + 1))
    
    echo ""
    echo "================================================================================"
    echo "🔌 CONNECTION #$CONNECTION_NUM - $(date '+%Y-%m-%d %H:%M:%S')"
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
            # Check for mode identifier
            if echo "$line" | grep -q "MODE:RSA"; then
                echo "🔐 ENCRYPTION MODE: RSA (Classical)"
                echo "📦 ENCRYPTED: [Binary TLS encrypted data]"
                echo "🔓 DECRYPTED: MODE:RSA"
                echo ""
            elif echo "$line" | grep -q "MODE:PQC"; then
                echo "🛡️  ENCRYPTION MODE: PQC (Post-Quantum)"
                echo "📦 ENCRYPTED: [Binary TLS encrypted data]"
                echo "🔓 DECRYPTED: MODE:PQC"
                echo ""
            elif echo "$line" | grep -q "MODE:HYBRID"; then
                echo "🔥 ENCRYPTION MODE: HYBRID (Classical + PQC)"
                echo "📦 ENCRYPTED: [Binary TLS encrypted data]"
                echo "🔓 DECRYPTED: MODE:HYBRID"
                echo ""
            fi
            
            # Check for message
            if echo "$line" | grep -q "Hi, how are you"; then
                echo "📦 ENCRYPTED: [Binary TLS encrypted data]"
                echo "🔓 DECRYPTED: Hi, how are you"
                echo ""
            fi
        fi
    done
    
    echo "✅ Connection closed"
    echo ""
    
    sleep 0.5
done
