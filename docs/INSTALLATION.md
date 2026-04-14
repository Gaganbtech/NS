# Installation Guide
## Post-Quantum Cryptography TLS Dashboard

This guide provides step-by-step instructions for setting up the PQC TLS Dashboard on various platforms.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Ubuntu/Debian Installation](#ubuntudebian-installation)
3. [macOS Installation](#macos-installation)
4. [Windows (WSL) Installation](#windows-wsl-installation)
5. [OQS-OpenSSL Installation](#oqs-openssl-installation)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS:** Linux (Ubuntu 20.04+), macOS (10.15+), or Windows 10/11 with WSL2
- **Python:** 3.8 or higher
- **RAM:** 2GB minimum, 4GB recommended
- **Disk Space:** 500MB for base installation, 2GB for OQS-OpenSSL
- **Network:** Internet connection for package downloads

### Software Dependencies
- Python 3.8+
- pip (Python package manager)
- OpenSSL 1.1.1+ or 3.0+
- Git
- Build tools (gcc, make, cmake) - for OQS compilation

---

## Ubuntu/Debian Installation

### Step 1: Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install Dependencies
```bash
# Install Python and pip
sudo apt install -y python3 python3-pip

# Install OpenSSL
sudo apt install -y openssl libssl-dev

# Install build tools (for OQS)
sudo apt install -y build-essential git cmake ninja-build

# Install network tools
sudo apt install -y netcat wireshark
```

### Step 3: Clone Repository
```bash
git clone <repository-url>
cd pqc-tls-dashboard
```

### Step 4: Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

### Step 5: Generate Certificates
```bash
cd scripts
chmod +x *.sh
./generate_certs.sh
cd ..
```

### Step 6: Test Basic Installation
```bash
# Terminal 1: Start server
cd scripts
./start_server.sh

# Terminal 2: Start dashboard
python3 app.py
```

---

## macOS Installation

### Step 1: Install Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Dependencies
```bash
# Install Python
brew install python@3.11

# Install OpenSSL
brew install openssl@3

# Install build tools
brew install cmake ninja git

# Install network tools
brew install netcat wireshark
```

### Step 3: Clone Repository
```bash
git clone <repository-url>
cd pqc-tls-dashboard
```

### Step 4: Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

### Step 5: Generate Certificates
```bash
cd scripts
chmod +x *.sh
./generate_certs.sh
cd ..
```

### Step 6: Configure OpenSSL Path (if needed)
```bash
# Add to ~/.zshrc or ~/.bash_profile
export PATH="/usr/local/opt/openssl@3/bin:$PATH"
export LDFLAGS="-L/usr/local/opt/openssl@3/lib"
export CPPFLAGS="-I/usr/local/opt/openssl@3/include"

# Reload shell
source ~/.zshrc
```

---

## Windows (WSL) Installation

### Step 1: Install WSL2
```powershell
# Run in PowerShell as Administrator
wsl --install -d Ubuntu-22.04
```

### Step 2: Open Ubuntu Terminal
```bash
# Update system
sudo apt update && sudo apt upgrade -y
```

### Step 3: Follow Ubuntu Installation Steps
Follow the [Ubuntu/Debian Installation](#ubuntudebian-installation) steps above.

### Step 4: Access Dashboard from Windows
- Dashboard will be accessible at: `http://localhost:5000`
- Use Windows browser to access WSL services

---

## OQS-OpenSSL Installation

OQS-OpenSSL provides post-quantum cryptography support. This is **optional** but **highly recommended** for full functionality.

### Automated Installation (Recommended)

```bash
cd scripts
./setup_oqs.sh
```

This script will:
1. Install dependencies
2. Clone and build liboqs
3. Clone and build OQS-OpenSSL
4. Configure environment variables
5. Verify installation

**Installation time:** 15-30 minutes depending on system

### Manual Installation

#### Step 1: Install Dependencies
```bash
# Ubuntu/Debian
sudo apt install -y build-essential git cmake ninja-build libssl-dev

# macOS
brew install cmake ninja openssl@3
```

#### Step 2: Build liboqs
```bash
mkdir -p ~/oqs-build
cd ~/oqs-build

git clone --depth 1 https://github.com/open-quantum-safe/liboqs.git
cd liboqs
mkdir build && cd build

cmake -GNinja \
    -DCMAKE_INSTALL_PREFIX=~/oqs-build/oqs \
    -DBUILD_SHARED_LIBS=ON \
    ..

ninja
ninja install
```

#### Step 3: Build OQS-OpenSSL
```bash
cd ~/oqs-build

git clone --depth 1 --branch OQS-OpenSSL_1_1_1-stable \
    https://github.com/open-quantum-safe/openssl.git
cd openssl

./Configure no-shared linux-x86_64 \
    -lm \
    --prefix=~/oqs-build/oqs-openssl

make -j$(nproc)
make install
```

#### Step 4: Update Environment
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/oqs-build/oqs-openssl/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/oqs-build/oqs/lib:$LD_LIBRARY_PATH"

# Reload
source ~/.bashrc
```

#### Step 5: Verify Installation
```bash
openssl version
# Should show OQS-OpenSSL version

openssl list -kem-algorithms | grep MLKEM
# Should show MLKEM768 and other PQC algorithms
```

---

## Verification

### Test 1: Check Python Installation
```bash
python3 --version
# Should show Python 3.8 or higher

pip3 --version
# Should show pip version
```

### Test 2: Check OpenSSL
```bash
openssl version
# Should show OpenSSL 1.1.1 or higher

# Check for PQC support (if OQS installed)
openssl list -kem-algorithms
```

### Test 3: Check Flask
```bash
python3 -c "import flask; print(flask.__version__)"
# Should print Flask version
```

### Test 4: Generate Test Certificate
```bash
cd scripts
./generate_certs.sh
# Should create certs/server.crt and certs/server.key
```

### Test 5: Start TLS Server
```bash
cd scripts
./start_server.sh
# Should start OpenSSL server on port 4433
# Press Ctrl+C to stop
```

### Test 6: Start Dashboard
```bash
python3 app.py
# Should start Flask on http://localhost:5000
# Open in browser
```

### Test 7: Run Connection Tests
```bash
cd scripts
./test_connection.sh
# Should test RSA, PQC, and Hybrid modes
```

---

## Troubleshooting

### Issue: Python not found
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip

# macOS
brew install python@3.11

# Verify
python3 --version
```

### Issue: OpenSSL not found
```bash
# Ubuntu/Debian
sudo apt install openssl libssl-dev

# macOS
brew install openssl@3

# Verify
openssl version
```

### Issue: Port 4433 already in use
```bash
# Find process using port
lsof -i :4433

# Kill process
kill -9 <PID>

# Or change port in scripts/start_server.sh
```

### Issue: Permission denied on scripts
```bash
chmod +x scripts/*.sh
```

### Issue: Flask not found
```bash
pip3 install flask
# or
pip3 install -r requirements.txt
```

### Issue: Certificate generation fails
```bash
# Check OpenSSL installation
openssl version

# Try manual generation
openssl req -x509 -newkey rsa:2048 \
    -keyout certs/server.key \
    -out certs/server.crt \
    -days 365 -nodes \
    -subj "/CN=localhost"
```

### Issue: OQS-OpenSSL build fails
```bash
# Install missing dependencies
sudo apt install -y build-essential cmake ninja-build

# Check disk space
df -h

# Check build logs
cat ~/oqs-build/openssl/config.log
```

### Issue: Cannot access dashboard from browser
```bash
# Check if Flask is running
ps aux | grep python

# Check firewall
sudo ufw status
sudo ufw allow 5000

# Try different port
python3 app.py --port 8080
```

### Issue: Wireshark permission denied
```bash
# Add user to wireshark group
sudo usermod -aG wireshark $USER

# Logout and login again

# Or run with sudo
sudo wireshark
```

---

## Post-Installation Steps

### 1. Configure Server IP
Edit `app.py` and update:
```python
SERVER_HOST = "your.server.ip"  # Change from 192.168.0.104
SERVER_PORT = "4433"
```

### 2. Set Up Firewall Rules
```bash
# Allow TLS server port
sudo ufw allow 4433

# Allow Flask dashboard
sudo ufw allow 5000
```

### 3. Configure for Remote Access
```bash
# Edit app.py to bind to all interfaces
app.run(debug=True, host='0.0.0.0', port=5000)
```

### 4. Set Up Systemd Service (Optional)
```bash
# Create service file
sudo nano /etc/systemd/system/pqc-dashboard.service

# Add content:
[Unit]
Description=PQC TLS Dashboard
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/pqc-tls-dashboard
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable pqc-dashboard
sudo systemctl start pqc-dashboard
```

---

## Next Steps

After successful installation:

1. **Read the README** - Understand project features
2. **Review Theory** - Check `docs/THEORY.md` for cryptographic background
3. **Run Tests** - Execute `scripts/test_connection.sh`
4. **Explore Dashboard** - Open http://localhost:5000
5. **Capture Traffic** - Use Wireshark to analyze packets
6. **Customize** - Modify scripts for your environment

---

## Support

If you encounter issues not covered here:

1. Check the main [README.md](../README.md)
2. Review error messages carefully
3. Check system logs: `journalctl -xe`
4. Verify all dependencies are installed
5. Try manual installation steps
6. Open an issue on GitHub with:
   - OS and version
   - Error messages
   - Steps to reproduce

---

**Installation complete! You're ready to analyze post-quantum cryptography.**
