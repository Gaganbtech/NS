#!/bin/bash
# Test TLS Connections - RSA, PQC, and Hybrid modes

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SERVER="192.168.0.104"
PORT="4433"

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              TLS CONNECTION TEST SUITE                        ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 1: RSA (Classical)
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TEST 1: RSA (Classical TLS)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

echo "Q" | timeout 5 openssl s_client -connect $SERVER:$PORT -showcerts 2>&1 | \
    grep -E "Cipher|Protocol|Server Temp Key|Verify return code" || \
    echo -e "${RED}❌ Connection failed${NC}"

echo ""
read -p "Press Enter to continue to Test 2..."

# Test 2: PQC (MLKEM768)
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TEST 2: PQC (MLKEM768/Kyber)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

echo "Q" | timeout 5 openssl s_client -connect $SERVER:$PORT -groups MLKEM768 -showcerts 2>&1 | \
    grep -E "Cipher|Protocol|Server Temp Key|Verify return code" || \
    echo -e "${RED}❌ Connection failed or PQC not supported${NC}"

echo ""
read -p "Press Enter to continue to Test 3..."

# Test 3: Hybrid (X25519 + MLKEM768)
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TEST 3: Hybrid (X25519 + MLKEM768)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

echo "Q" | timeout 5 openssl s_client -connect $SERVER:$PORT -groups X25519MLKEM768 -showcerts 2>&1 | \
    grep -E "Cipher|Protocol|Server Temp Key|Verify return code" || \
    echo -e "${RED}❌ Connection failed or Hybrid mode not supported${NC}"

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  ALL TESTS COMPLETED                          ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
