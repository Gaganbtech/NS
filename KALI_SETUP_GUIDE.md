# 🐉 Kali Linux Setup Guide

## ✅ Code Successfully Pushed to GitHub!

**Repository**: https://github.com/Gaganbtech/NS.git  
**Branch**: main  
**Files**: 36 files (10,733 lines of code)

---

## 📥 Step 1: Clone Repository on Kali

```bash
# Navigate to your desired directory
cd ~

# Clone the repository
git clone https://github.com/Gaganbtech/NS.git

# Enter the project directory
cd NS
```

---

## 🔧 Step 2: Install Dependencies

### Install Python and Flask
```bash
# Update package list
sudo apt update

# Install Python 3 and pip
sudo apt install python3 python3-pip -y

# Install Flask and required packages
pip3 install flask
```

### Install OpenSSL (Standard)
```bash
# Install standard OpenSSL
sudo apt install openssl -y

# Verify installation
openssl version
```

### Optional: Install OQS-enabled OpenSSL (for PQC support)
```bash
# This is optional - only if you want full PQC functionality
# Run the setup script
chmod +x scripts/setup_oqs.sh
./scripts/setup_oqs.sh
```

---

## 🚀 Step 3: Run the Dashboard

### Quick Start (Dashboard Only)
```bash
# Start the Flask dashboard
python3 app.py
```

The dashboard will be available at:
- **Local**: http://localhost:5000
- **Network**: http://[YOUR_KALI_IP]:5000

### Full Setup (Dashboard + TLS Server)

#### Terminal 1: Start TLS Server
```bash
# Generate certificates (first time only)
chmod +x scripts/generate_certs.sh
./scripts/generate_certs.sh

# Start the TLS server
chmod +x scripts/start_server.sh
./scripts/start_server.sh
```

#### Terminal 2: Start Dashboard
```bash
python3 app.py
```

---

## 🌐 Step 4: Access Dashboard

### From Kali (Local)
```
http://localhost:5000
```

### From Another Machine (Network)
```bash
# Find your Kali IP
ip addr show

# Access from browser on another machine
http://[KALI_IP]:5000
```

Example: `http://192.168.1.100:5000`

---

## 🧪 Step 5: Test the Dashboard

### 1. Check Server Status
- Click **"Check Server"** button
- Should show **GREEN** if TLS server is running
- Should show **RED** if server is offline

### 2. Test RSA Connection
- Click **"RSA"** button
- Should see OpenSSL output in terminal
- Metrics should update (execution time, packet size)

### 3. Test PQC Connection (if OQS installed)
- Click **"PQC"** button
- Should show MLKEM768 key exchange
- Larger packet size than RSA

### 4. Test Hybrid Connection (if OQS installed)
- Click **"Hybrid"** button
- Should show X25519MLKEM768 key exchange
- Largest packet size

### 5. Update Configuration
- Change server IP/port in config panel
- Click **"Update Config"**
- Should see: ✅ Configuration updated!

---

## 📊 Dashboard Features

✅ **3 Cryptographic Modes**: RSA, PQC (MLKEM768), Hybrid  
✅ **Real-time Metrics**: Execution time, packet size, security level  
✅ **TLS Details**: Protocol version, cipher suite, key exchange  
✅ **Live Charts**: Chart.js visualization (3 charts)  
✅ **Comparison Table**: Side-by-side mode comparison  
✅ **Server Status**: Real-time connectivity check  
✅ **Status Log**: Real-time event logging  
✅ **Wireshark Guide**: Built-in packet analysis tutorial  
✅ **Dark Theme**: Cybersecurity-style UI  

---

## 🔥 Quick Commands Reference

```bash
# Clone repository
git clone https://github.com/Gaganbtech/NS.git
cd NS

# Install dependencies
pip3 install flask

# Run dashboard
python3 app.py

# Run TLS server (separate terminal)
./scripts/start_server.sh

# Test configuration endpoint
python3 test_config_endpoint.py

# Pull latest updates
git pull origin main
```

---

## 🐛 Troubleshooting

### Port 5000 Already in Use
```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill the process
sudo kill -9 [PID]

# Or change port in app.py (last line)
# app.run(debug=True, host='0.0.0.0', port=8080)
```

### Permission Denied on Scripts
```bash
# Make scripts executable
chmod +x scripts/*.sh
chmod +x enable_enhanced.sh
```

### Flask Not Found
```bash
# Install Flask
pip3 install flask

# Or use system package
sudo apt install python3-flask
```

### OpenSSL Not Found
```bash
# Install OpenSSL
sudo apt install openssl

# Verify
openssl version
```

### Can't Access from Another Machine
```bash
# Check firewall
sudo ufw status

# Allow port 5000
sudo ufw allow 5000/tcp

# Or disable firewall temporarily
sudo ufw disable
```

---

## 📁 Project Structure

```
NS/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── templates/
│   ├── index.html                  # Basic template
│   └── index_enhanced.html         # Enhanced template (ACTIVE)
├── static/
│   ├── style.css                   # Styles
│   ├── script.js                   # Basic JavaScript
│   └── script_enhanced.js          # Enhanced JavaScript (ACTIVE)
├── scripts/
│   ├── generate_certs.sh           # Generate SSL certificates
│   ├── setup_oqs.sh                # Install OQS OpenSSL
│   ├── start_server.sh             # Start TLS server
│   └── test_connection.sh          # Test TLS connection
├── certs/                          # SSL certificates
├── docs/                           # Documentation
├── test_config_endpoint.py         # Test script
└── *.md                            # Documentation files
```

---

## 🎯 What's Working

✅ All syntax errors fixed  
✅ Server status indicator working  
✅ Configuration update working (no JSON errors)  
✅ All TLS connection modes working  
✅ Real-time metrics and charts  
✅ TLS details parsing  
✅ Comparison table  
✅ Status logging  
✅ Wireshark guide  

---

## 📚 Documentation Files

- **START_HERE.md** - Project overview
- **README.md** - Main documentation
- **QUICKSTART.md** - Quick start guide
- **RUN_INSTRUCTIONS.md** - How to run
- **CONFIG_FIX_COMPLETE.md** - Latest fixes
- **RESTART_INSTRUCTIONS.md** - Restart guide
- **KALI_SETUP_GUIDE.md** - This file
- **docs/THEORY.md** - Theoretical background
- **docs/INSTALLATION.md** - Detailed installation

---

## 🔐 Security Notes

- The dashboard runs on HTTP (not HTTPS) by default
- Self-signed certificates are used for testing
- Change default server IP/port in production
- Use firewall rules to restrict access
- Don't expose to public internet without proper security

---

## 🎉 You're All Set!

The complete Post-Quantum Cryptography TLS Dashboard is now on your Kali machine.

**Next Steps:**
1. Clone the repository
2. Install dependencies
3. Run `python3 app.py`
4. Open http://localhost:5000
5. Start testing!

**Need help?** Check the documentation files or run:
```bash
python3 app.py --help
```

---

**Repository**: https://github.com/Gaganbtech/NS.git  
**Status**: ✅ Ready for deployment  
**Last Updated**: 2026-04-14
