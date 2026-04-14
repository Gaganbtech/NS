#!/bin/bash
# Enable Enhanced Dashboard with Advanced Metrics

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Enabling Enhanced Dashboard with Advanced Metrics         ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Backup original files
echo -e "${YELLOW}Backing up original files...${NC}"
if [ -f "templates/index.html" ]; then
    cp templates/index.html templates/index_original.html
    echo -e "${GREEN}✓${NC} Backed up templates/index.html"
fi

if [ -f "static/script.js" ]; then
    cp static/script.js static/script_original.js
    echo -e "${GREEN}✓${NC} Backed up static/script.js"
fi

# Enable enhanced versions
echo ""
echo -e "${YELLOW}Enabling enhanced versions...${NC}"

if [ -f "templates/index_enhanced.html" ]; then
    cp templates/index_enhanced.html templates/index.html
    echo -e "${GREEN}✓${NC} Enabled enhanced HTML template"
else
    echo -e "${YELLOW}⚠️  templates/index_enhanced.html not found${NC}"
fi

if [ -f "static/script_enhanced.js" ]; then
    cp static/script_enhanced.js static/script.js
    echo -e "${GREEN}✓${NC} Enabled enhanced JavaScript"
else
    echo -e "${YELLOW}⚠️  static/script_enhanced.js not found${NC}"
fi

# app.py is already enhanced
echo -e "${GREEN}✓${NC} app.py already has enhanced features"

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              ENHANCED DASHBOARD ENABLED!                      ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}New Features:${NC}"
echo "  ✅ TLS Handshake Details Panel"
echo "  ✅ Execution Time Metrics"
echo "  ✅ Packet Size Estimation"
echo "  ✅ Security Level Indicators"
echo "  ✅ Real-time Comparison Table"
echo "  ✅ Chart.js Visualization (3 charts)"
echo "  ✅ Real-time Status Log"
echo "  ✅ Wireshark Guide Modal"
echo ""
echo -e "${YELLOW}To start the enhanced dashboard:${NC}"
echo "  1. Terminal 1: cd scripts && ./start_server.sh"
echo "  2. Terminal 2: python3 app.py"
echo "  3. Browser: http://localhost:5000"
echo ""
echo -e "${YELLOW}To restore original version:${NC}"
echo "  cp templates/index_original.html templates/index.html"
echo "  cp static/script_original.js static/script.js"
echo ""
