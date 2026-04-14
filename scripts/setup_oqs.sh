#!/bin/bash
# Setup Script for OQS-OpenSSL (Post-Quantum Cryptography Support)
# This script installs OpenSSL with OQS (Open Quantum Safe) support

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     OQS-OpenSSL Installation Script                           ║${NC}"
echo -e "${BLUE}║     Post-Quantum Cryptography Support                         ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo -e "${GREEN}✓${NC} Detected: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    echo -e "${GREEN}✓${NC} Detected: macOS"
else
    echo -e "${RED}❌ Unsupported OS: $OSTYPE${NC}"
    exit 1
fi

# Install dependencies
echo ""
echo -e "${BLUE}Installing dependencies...${NC}"

if [ "$OS" = "linux" ]; then
    sudo apt update
    sudo apt install -y build-essential git cmake ninja-build \
        libssl-dev python3 python3-pip
elif [ "$OS" = "macos" ]; then
    if ! command -v brew &> /dev/null; then
        echo -e "${RED}❌ Homebrew not found. Please install Homebrew first.${NC}"
        exit 1
    fi
    brew install cmake ninja openssl@3
fi

echo -e "${GREEN}✓${NC} Dependencies installed"

# Create build directory
BUILD_DIR="$HOME/oqs-build"
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

# Clone and build liboqs
echo ""
echo -e "${BLUE}Building liboqs...${NC}"

if [ -d "liboqs" ]; then
    echo "Removing existing liboqs directory..."
    rm -rf liboqs
fi

git clone --depth 1 https://github.com/open-quantum-safe/liboqs.git
cd liboqs
mkdir -p build && cd build

cmake -GNinja \
    -DCMAKE_INSTALL_PREFIX="$BUILD_DIR/oqs" \
    -DBUILD_SHARED_LIBS=ON \
    ..

ninja
ninja install

echo -e "${GREEN}✓${NC} liboqs built successfully"

# Clone and build OQS-OpenSSL
echo ""
echo -e "${BLUE}Building OQS-OpenSSL...${NC}"

cd "$BUILD_DIR"

if [ -d "openssl" ]; then
    echo "Removing existing openssl directory..."
    rm -rf openssl
fi

git clone --depth 1 --branch OQS-OpenSSL_1_1_1-stable \
    https://github.com/open-quantum-safe/openssl.git
cd openssl

./Configure no-shared linux-x86_64 \
    -lm \
    --prefix="$BUILD_DIR/oqs-openssl"

make -j$(nproc 2>/dev/null || sysctl -n hw.ncpu)
make install

echo -e "${GREEN}✓${NC} OQS-OpenSSL built successfully"

# Update PATH
echo ""
echo -e "${BLUE}Updating environment...${NC}"

SHELL_RC="$HOME/.bashrc"
if [ "$OS" = "macos" ]; then
    SHELL_RC="$HOME/.zshrc"
fi

if ! grep -q "oqs-openssl/bin" "$SHELL_RC"; then
    echo "" >> "$SHELL_RC"
    echo "# OQS-OpenSSL" >> "$SHELL_RC"
    echo "export PATH=\"$BUILD_DIR/oqs-openssl/bin:\$PATH\"" >> "$SHELL_RC"
    echo "export LD_LIBRARY_PATH=\"$BUILD_DIR/oqs/lib:\$LD_LIBRARY_PATH\"" >> "$SHELL_RC"
fi

# Verify installation
echo ""
echo -e "${BLUE}Verifying installation...${NC}"

export PATH="$BUILD_DIR/oqs-openssl/bin:$PATH"
export LD_LIBRARY_PATH="$BUILD_DIR/oqs/lib:$LD_LIBRARY_PATH"

if "$BUILD_DIR/oqs-openssl/bin/openssl" version | grep -q "OpenSSL"; then
    echo -e "${GREEN}✓${NC} OQS-OpenSSL installed successfully"
    echo ""
    echo "Version: $("$BUILD_DIR/oqs-openssl/bin/openssl" version)"
else
    echo -e "${RED}❌ Installation verification failed${NC}"
    exit 1
fi

# Check for PQC algorithms
echo ""
echo -e "${BLUE}Checking PQC algorithm support...${NC}"

if "$BUILD_DIR/oqs-openssl/bin/openssl" list -kem-algorithms 2>/dev/null | grep -q "MLKEM"; then
    echo -e "${GREEN}✓${NC} MLKEM (Kyber) support detected"
else
    echo -e "${YELLOW}⚠️  MLKEM support not detected${NC}"
fi

# Installation complete
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              INSTALLATION COMPLETE!                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}IMPORTANT:${NC} Restart your terminal or run:"
echo "  source $SHELL_RC"
echo ""
echo "Installation directory: $BUILD_DIR"
echo "OpenSSL binary: $BUILD_DIR/oqs-openssl/bin/openssl"
echo ""
echo "To use OQS-OpenSSL, either:"
echo "  1. Restart your terminal (recommended)"
echo "  2. Run: export PATH=\"$BUILD_DIR/oqs-openssl/bin:\$PATH\""
echo ""
echo "Test with: openssl version"
echo ""
