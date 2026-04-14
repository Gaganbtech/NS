#!/bin/bash

# TLS Server with Connection Logging
# Detects RSA, PQC, or Hybrid based on client request

echo "================================================================================"
echo "  🔐 TLS SERVER - MODE DETECTOR"
echo "================================================================================"
echo ""
echo "  Listening on: 0.0.0.0:4433"
echo "  Detecting: RSA, PQC (MLKEM768), Hybrid (X25519MLKEM768)"
echo ""
echo "================================================================================"
echo ""

# Create named pipe for logging
LOGFILE="/tmp/tls_server_$$.log"

# Start OpenSSL server in background and capture output
openssl s_server \
    -accept 4433 \
    -cert certs/server.crt \
    -key certs/server.key \
    -state \
    -msg \
    -tlsextdebug \
    -groups X25519:MLKEM768:X25519MLKEM768 \
    2>&1 | while IFS= read -r line; do
    
    # Detect new connection
    if echo "$line" | grep -q "ACCEPT"; then
        echo ""
        echo "================================================================================"
        echo "🔌 NEW CONNECTION - $(date '+%Y-%m-%d %H:%M:%S')"
        echo "================================================================================"
        echo "⏳ Analyzing encryption method..."
        MODE=""
    fi
    
    # Detect supported groups from client
    if echo "$line" | grep -qi "supported_groups"; then
        if echo "$line" | grep -qi "x25519mlkem768"; then
            MODE="HYBRID"
        elif echo "$line" | grep -qi "mlkem768"; then
            MODE="PQC"
        elif echo "$line" | grep -qi "x25519"; then
            MODE="RSA"
        fi
    fi
    
    # Detect key share
    if echo "$line" | grep -qi "key_share"; then
        if echo "$line" | grep -qi "x25519mlkem768"; then
            MODE="HYBRID"
        elif echo "$line" | grep -qi "mlkem768"; then
            MODE="PQC"
        elif echo "$line" | grep -qi "x25519"; then
            MODE="RSA"
        fi
    fi
    
    # Detect Server Temp Key
    if echo "$line" | grep -q "Server Temp Key:"; then
        KEY=$(echo "$line" | sed 's/.*Server Temp Key: //')
        
        if echo "$KEY" | grep -qi "x25519mlkem768"; then
            MODE="HYBRID"
        elif echo "$KEY" | grep -qi "mlkem768"; then
            MODE="PQC"
        elif echo "$KEY" | grep -qi "x25519"; then
            MODE="RSA"
        fi
        
        # Display mode
        if [ "$MODE" = "HYBRID" ]; then
            echo ""
            echo "🔥 ============================================================================"
            echo "   ENCRYPTION MODE: HYBRID (CLASSICAL + POST-QUANTUM)"
            echo "   ────────────────────────────────────────────────────────────────────────────"
            echo "   Button Clicked: HYBRID"
            echo "   Key Exchange:   X25519 + MLKEM768"
            echo "   Security Level: ⭐⭐⭐ MAXIMUM (Quantum-Resistant)"
            echo "============================================================================"
            echo ""
        elif [ "$MODE" = "PQC" ]; then
            echo ""
            echo "🛡️  ============================================================================"
            echo "   ENCRYPTION MODE: PQC (POST-QUANTUM)"
            echo "   ────────────────────────────────────────────────────────────────────────────"
            echo "   Button Clicked: PQC"
            echo "   Key Exchange:   MLKEM768 (Kyber)"
            echo "   Security Level: ⭐⭐ HIGH (Quantum-Resistant)"
            echo "============================================================================"
            echo ""
        elif [ "$MODE" = "RSA" ]; then
            echo ""
            echo "🔐 ============================================================================"
            echo "   ENCRYPTION MODE: RSA (CLASSICAL)"
            echo "   ────────────────────────────────────────────────────────────────────────────"
            echo "   Button Clicked: RSA"
            echo "   Key Exchange:   X25519 (Elliptic Curve)"
            echo "   Security Level: ⭐ MEDIUM (Vulnerable to Quantum)"
            echo "============================================================================"
            echo ""
        fi
    fi
    
    # Detect message
    if echo "$line" | grep -q "Hi, how are you"; then
        echo "💬 ============================================================================"
        echo "   MESSAGE RECEIVED (DECRYPTED):"
        echo "   ────────────────────────────────────────────────────────────────────────────"
        echo "   >>> Hi, how are you <<<"
        echo "============================================================================"
        echo ""
    fi
    
    # Show other important lines
    if echo "$line" | grep -q "Cipher"; then
        echo "🔐 Cipher: $(echo "$line" | sed 's/.*Cipher: //')"
    fi
    
    if echo "$line" | grep -q "Protocol"; then
        echo "📡 Protocol: $(echo "$line" | sed 's/.*Protocol: //')"
    fi
    
done
