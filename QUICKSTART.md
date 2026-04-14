# Quick Start Guide
## Get Running in 5 Minutes

This guide gets you up and running with the PQC TLS Dashboard as quickly as possible.

---

## Prerequisites Check

```bash
# Check Python (need 3.8+)
python3 --version

# Check OpenSSL (need 1.1.1+)
openssl version

# Check pip
pip3 --version
```

If any are missing, see [INSTALLATION.md](docs/INSTALLATION.md).

---

## 5-Minute Setup

### Step 1: Install Flask (30 seconds)
```bash
pip3 install flask
```

### Step 2: Generate Certificates (30 seconds)
```bash
cd scripts
chmod +x *.sh
./generate_certs.sh
cd ..
```

### Step 3: Start TLS Server (Terminal 1)
```bash
cd scripts
./start_server.sh
```

Leave this running. Open a new terminal for Step 4.

### Step 4: Start Dashboard (Terminal 2)
```bash
python3 app.py
```

### Step 5: Open Browser
```
http://localhost:5000
```

---

## First Test

1. Click **"Check Server"** button - should show "Online"
2. Click **"RSA"** button - should see TLS connection output
3. Check the terminal output for cipher suite information

---

## What You'll See

### Dashboard
- Modern dark theme cybersecurity interface
- Three buttons: RSA, PQC, Hybrid
- Real-time terminal output
- Connection status indicators

### Terminal Output
```
Cipher    : ECDHE-RSA-AES256-GCM-SHA384
Protocol  : TLSv1.3
Server Temp Key: X25519, 253 bits
Verify return code: 0 (ok)
```

---

## Troubleshooting

### Server won't start
```bash
# Check if port is in use
lsof -i :4433

# Kill existing process
kill -9 <PID>
```

### Dashboard won't start
```bash
# Install Flask
pip3 install flask

# Check port 5000
lsof -i :5000
```

### Connection fails
```bash
# Verify server is running
nc -zv localhost 4433

# Check firewall
sudo ufw allow 4433
```

---

## Next Steps

### Enable Post-Quantum Cryptography

For full PQC support (MLKEM768/Kyber), install OQS-OpenSSL:

```bash
cd scripts
./setup_oqs.sh
```

This takes 15-30 minutes but enables the **PQC** and **Hybrid** buttons.

### Capture Network Traffic

```bash
# Start Wireshark
sudo wireshark

# Filter: tcp.port == 4433
# Run tests from dashboard
# Analyze TLS handshake packets
```

### Run Automated Tests

```bash
cd scripts
./test_connection.sh
```

---

## Configuration

### Change Server IP/Port

Edit `app.py`:
```python
SERVER_HOST = "192.168.0.104"  # Your server IP
SERVER_PORT = "4433"           # Your port
```

Or use the dashboard config panel.

### Use Different Port

Edit `scripts/start_server.sh`:
```bash
PORT=8443  # Change from 4433
```

---

## Common Commands

```bash
# Start server
cd scripts && ./start_server.sh

# Start dashboard
python3 app.py

# Test RSA
echo "Q" | openssl s_client -connect localhost:4433

# Test PQC (requires OQS)
echo "Q" | openssl s_client -connect localhost:4433 -groups MLKEM768

# Test Hybrid (requires OQS)
echo "Q" | openssl s_client -connect localhost:4433 -groups X25519MLKEM768

# Run all tests
cd scripts && ./test_connection.sh

# Generate new certificates
cd scripts && ./generate_certs.sh
```

---

## Project Structure

```
pqc-tls-dashboard/
├── app.py              # Flask application (START HERE)
├── templates/
│   └── index.html      # Web interface
├── static/
│   ├── style.css       # Styling
│   └── script.js       # Client logic
├── scripts/
│   ├── start_server.sh # TLS server
│   ├── setup_oqs.sh    # Install PQC support
│   └── test_connection.sh # Run tests
└── certs/
    ├── server.crt      # SSL certificate
    └── server.key      # Private key
```

---

## Demo Flow

### For Presentations

1. **Show Dashboard** - Modern UI, explain three modes
2. **Test RSA** - Click RSA button, show classical TLS
3. **Explain Quantum Threat** - Why RSA is vulnerable
4. **Test PQC** - Click PQC button, show MLKEM768
5. **Test Hybrid** - Click Hybrid, explain defense-in-depth
6. **Show Wireshark** - Capture and analyze packets
7. **Compare Results** - Discuss cipher suites and key exchange

### For Viva/Defense

1. Explain project architecture
2. Demonstrate real TLS communication
3. Show OpenSSL commands
4. Analyze Wireshark captures
5. Discuss quantum threat and PQC solutions
6. Show code structure and implementation

---

## Key Features to Highlight

✅ **Real TLS** - Not simulation, actual OpenSSL connections  
✅ **Three Modes** - RSA, PQC (MLKEM768), Hybrid  
✅ **Modern UI** - Professional dashboard with real-time output  
✅ **Industry Tools** - OpenSSL, OQS, Wireshark  
✅ **Automated** - One-command setup and testing  
✅ **Educational** - Clear explanations and documentation  

---

## Getting Help

- **README.md** - Full documentation
- **docs/INSTALLATION.md** - Detailed setup guide
- **docs/THEORY.md** - Cryptographic background
- **Troubleshooting** - See INSTALLATION.md

---

## Success Checklist

- [ ] Python 3.8+ installed
- [ ] OpenSSL installed
- [ ] Flask installed (`pip3 install flask`)
- [ ] Certificates generated (`./scripts/generate_certs.sh`)
- [ ] Server starts (`./scripts/start_server.sh`)
- [ ] Dashboard starts (`python3 app.py`)
- [ ] Browser opens http://localhost:5000
- [ ] RSA test works (green output)
- [ ] (Optional) OQS-OpenSSL installed for PQC

---

**You're ready! Start exploring post-quantum cryptography.**

For full documentation, see [README.md](README.md).
