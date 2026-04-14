#!/bin/bash
# Start TLS Server with OpenSSL
# Supports RSA, PQC (MLKEM768), and Hybrid modes

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
PORT=4433
CERT_DIR="../certs"
CERT_FILE="$CERT_DIR/server.crt"
KEY_FILE="$CERT_DIR/server.key"

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         TLS SERVER STARTUP - OpenSSL/OQS                      ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if OpenSSL is installed
if ! command -v openssl &> /dev/null; then
    echo -e "${RED}❌ ERROR: OpenSSL not found${NC}"
    echo "Please install OpenSSL first:"
    echo "  Ubuntu/Debian: sudo apt install openssl"
    echo "  macOS: brew install openssl"
    exit 1
fi

echo -e "${GREEN}✓${NC} OpenSSL found: $(openssl version)"

# Check if certificates exist
if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
    echo -e "${YELLOW}⚠️  Certificates not found. Generating self-signed certificate...${NC}"
    mkdir -p "$CERT_DIR"
    
    openssl req -x509 -newkey rsa:2048 -keyout "$KEY_FILE" -out "$CERT_FILE" \
        -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=PQC-Lab/OU=Research/CN=localhost"
    
    echo -e "${GREEN}✓${NC} Certificate generated"
fi

# Check for OQS support
echo ""
echo -e "${BLUE}Checking for Post-Quantum Cryptography support...${NC}"
if openssl list -kem-algorithms 2>/dev/null | grep -q "MLKEM"; then
    echo -e "${GREEN}✓${NC} OQS-OpenSSL detected - PQC support available"
    PQC_SUPPORT=true
else
    echo -e "${YELLOW}⚠️  OQS-OpenSSL not detected - PQC modes will not work${NC}"
    echo "To enable PQC, install OQS-OpenSSL:"
    echo "  https://github.com/open-quantum-safe/openssl"
    PQC_SUPPORT=false
fi

# Start server
echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    STARTING TLS SERVER                        ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Server Configuration:${NC}"
echo "  Port: $PORT"
echo "  Certificate: $CERT_FILE"
echo "  Key: $KEY_FILE"
echo ""
echo -e "${GREEN}Supported Modes:${NC}"
echo "  ✓ RSA (Classical TLS)"
if [ "$PQC_SUPPORT" = true ]; then
    echo "  ✓ MLKEM768 (Post-Quantum)"
    echo "  ✓ X25519MLKEM768 (Hybrid)"
else
    echo "  ✗ MLKEM768 (Requires OQS-OpenSSL)"
    echo "  ✗ X25519MLKEM768 (Requires OQS-OpenSSL)"
fi
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Start OpenSSL server
if [ "$PQC_SUPPORT" = true ]; then
    # With PQC support - enable all groups
    openssl s_server \
        -cert "$CERT_FILE" \
        -key "$KEY_FILE" \
        -port $PORT \
        -groups X25519MLKEM768:MLKEM768:X25519:prime256v1 \
        -www \
        -state \
        -debug
else
    # Without PQC support - classical only
    openssl s_server \
        -cert "$CERT_FILE" \
        -key "$KEY_FILE" \
        -port $PORT \
        -www \
        -state \
        -debug
fi
