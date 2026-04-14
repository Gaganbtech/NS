#!/bin/bash

# TLS Server with Packet Capture Analysis
# Clearly shows RSA, PQC, or Hybrid mode

echo "================================================================================"
echo "  🔐 TLS SERVER WITH PACKET ANALYSIS"
echo "================================================================================"
echo ""
echo "  Starting server on port 4433..."
echo "  Capturing packets to analyze encryption mode..."
echo ""
echo "================================================================================"
echo ""

# Start packet capture in background
sudo tcpdump -i any -n port 4433 -A 2>/dev/null | while read line; do
    if echo "$line" | grep -q "mlkem768"; then
        if echo "$line" | grep -q "x25519"; then
            echo ""
            echo "🔥 ============================================================================"
            echo "   DETECTED: HYBRID MODE (X25519 + MLKEM768)"
            echo "   Button Clicked: HYBRID"
            echo "   Security: ⭐⭐⭐ MAXIMUM"
            echo "============================================================================"
            echo ""
        else
            echo ""
            echo "🛡️  ============================================================================"
            echo "   DETECTED: PQC MODE (MLKEM768)"
            echo "   Button Clicked: PQC"
            echo "   Security: ⭐⭐ HIGH"
            echo "============================================================================"
            echo ""
        fi
    elif echo "$line" | grep -q "x25519" && ! echo "$line" | grep -q "mlkem"; then
        echo ""
        echo "🔐 ============================================================================"
        echo "   DETECTED: RSA MODE (X25519)"
        echo "   Button Clicked: RSA"
        echo "   Security: ⭐ MEDIUM"
        echo "============================================================================"
        echo ""
    fi
    
    if echo "$line" | grep -q "Hi, how are you"; then
        echo "💬 MESSAGE: Hi, how are you"
        echo ""
    fi
done &

TCPDUMP_PID=$!

# Start OpenSSL server
openssl s_server \
    -accept 4433 \
    -cert certs/server.crt \
    -key certs/server.key \
    -quiet

# Cleanup
kill $TCPDUMP_PID 2>/dev/null
