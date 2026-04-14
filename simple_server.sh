#!/bin/bash

# Simple TLS Server - Just show connections and messages

echo "================================================================================"
echo "  🔐 TLS SERVER - LISTENING ON PORT 4433"
echo "================================================================================"
echo ""
echo "  Waiting for connections from Kali..."
echo "  Check the Kali dashboard to see which mode is being used!"
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
    echo "📡 Receiving data..."
    echo ""
    
    # Start server and capture output
    timeout 10 openssl s_server \
        -accept 4433 \
        -cert certs/server.crt \
        -key certs/server.key \
        -quiet \
        2>&1 | while IFS= read -r line; do
        
        # Show received data
        if [ ! -z "$line" ]; then
            echo "📨 Received: $line"
            
            # Check for mode indicators
            if echo "$line" | grep -qi "MODE:RSA"; then
                echo ""
                echo "🔐 ============================================================================"
                echo "   ENCRYPTION MODE: RSA (CLASSICAL)"
                echo "   Security: ⭐ MEDIUM"
                echo "============================================================================"
                echo ""
            elif echo "$line" | grep -qi "MODE:PQC"; then
                echo ""
                echo "🛡️  ============================================================================"
                echo "   ENCRYPTION MODE: PQC (POST-QUANTUM)"
                echo "   Security: ⭐⭐ HIGH"
                echo "============================================================================"
                echo ""
            elif echo "$line" | grep -qi "MODE:HYBRID"; then
                echo ""
                echo "🔥 ============================================================================"
                echo "   ENCRYPTION MODE: HYBRID"
                echo "   Security: ⭐⭐⭐ MAXIMUM"
                echo "============================================================================"
                echo ""
            fi
            
            # Check for message
            if echo "$line" | grep -q "Hi, how are you"; then
                echo ""
                echo "💬 ============================================================================"
                echo "   MESSAGE RECEIVED: Hi, how are you"
                echo "============================================================================"
                echo ""
            fi
        fi
    done
    
    echo ""
    echo "✅ Connection closed"
    echo ""
    
    # Small delay before accepting next connection
    sleep 0.5
done
