#!/bin/bash
# Generate SSL/TLS Certificates for Testing

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

CERT_DIR="../certs"

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           SSL/TLS Certificate Generator                       ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Create directory
mkdir -p "$CERT_DIR"

# Generate private key
echo -e "${BLUE}Generating RSA private key...${NC}"
openssl genrsa -out "$CERT_DIR/server.key" 2048
echo -e "${GREEN}✓${NC} Private key generated"

# Generate certificate signing request
echo ""
echo -e "${BLUE}Generating certificate signing request...${NC}"
openssl req -new -key "$CERT_DIR/server.key" -out "$CERT_DIR/server.csr" \
    -subj "/C=US/ST=California/L=San Francisco/O=PQC Research Lab/OU=Network Security/CN=localhost"
echo -e "${GREEN}✓${NC} CSR generated"

# Generate self-signed certificate
echo ""
echo -e "${BLUE}Generating self-signed certificate...${NC}"
openssl x509 -req -days 365 \
    -in "$CERT_DIR/server.csr" \
    -signkey "$CERT_DIR/server.key" \
    -out "$CERT_DIR/server.crt"
echo -e "${GREEN}✓${NC} Certificate generated"

# Display certificate info
echo ""
echo -e "${BLUE}Certificate Information:${NC}"
openssl x509 -in "$CERT_DIR/server.crt" -text -noout | grep -E "Subject:|Issuer:|Not Before|Not After"

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              CERTIFICATES GENERATED SUCCESSFULLY              ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Files created:"
echo "  • $CERT_DIR/server.key (Private Key)"
echo "  • $CERT_DIR/server.crt (Certificate)"
echo "  • $CERT_DIR/server.csr (Certificate Signing Request)"
echo ""
