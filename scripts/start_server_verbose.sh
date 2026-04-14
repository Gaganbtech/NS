#!/bin/bash

# Enhanced TLS Server with Clear Message Display
# Shows: Key Exchange, Cipher, and Received Messages

echo "=========================================="
echo "  TLS SERVER - VERBOSE MODE"
echo "=========================================="
echo ""
echo "Listening on port 4433..."
echo "Waiting for connections..."
echo ""
echo "Key Exchange Methods:"
echo "  - RSA Mode: X25519 (Classical)"
echo "  - PQC Mode: MLKEM768 (Quantum-Safe)"
echo "  - Hybrid Mode: X25519MLKEM768 (Both)"
echo ""
echo "=========================================="
echo ""

# Start OpenSSL server with verbose output
openssl s_server \
    -accept 4433 \
    -cert certs/server.crt \
    -key certs/server.key \
    -state \
    -msg \
    -debug \
    -tlsextdebug \
    2>&1 | while IFS= read -r line; do
        # Highlight key exchange
        if echo "$line" | grep -q "Server Temp Key"; then
            echo ""
            echo "🔑 ============================================"
            echo "   KEY EXCHANGE DETECTED:"
            echo "   $line"
            echo "============================================"
            echo ""
        # Highlight cipher
        elif echo "$line" | grep -q "Cipher"; then
            echo ""
            echo "🔐 ============================================"
            echo "   CIPHER SUITE:"
            echo "   $line"
            echo "============================================"
            echo ""
        # Highlight protocol
        elif echo "$line" | grep -q "Protocol"; then
            echo ""
            echo "📡 ============================================"
            echo "   PROTOCOL VERSION:"
            echo "   $line"
            echo "============================================"
            echo ""
        # Highlight received data
        elif echo "$line" | grep -q "read from"; then
            echo ""
            echo "📨 ============================================"
            echo "   MESSAGE RECEIVED FROM CLIENT"
            echo "============================================"
        # Show the actual message
        elif echo "$line" | grep -qi "Hi, how are you"; then
            echo ""
            echo "💬 ============================================"
            echo "   DECRYPTED MESSAGE:"
            echo "   >>> Hi, how are you <<<"
            echo "============================================"
            echo ""
        else
            echo "$line"
        fi
    done
