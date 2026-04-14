# 🔍 How to See Encryption Details Clearly

## **Method 1: Enhanced Python Server (BEST)**

**On Mac:**
```bash
cd ~/Desktop/"Gagan NS prjt"
python3 tls_server_enhanced.py
```

**Output will show:**
```
================================================================================
  🔐 POST-QUANTUM CRYPTOGRAPHY TLS SERVER - ENHANCED MODE
================================================================================

  Listening on: 0.0.0.0:4433
  
  Supported Key Exchange Methods:
    ✓ RSA Mode      → X25519 (Classical Elliptic Curve)
    ✓ PQC Mode      → MLKEM768 (Post-Quantum Kyber)
    ✓ Hybrid Mode   → X25519MLKEM768 (Classical + PQC)

================================================================================

⏳ Waiting for connections...

================================================================================
🔌 NEW CONNECTION ESTABLISHED - 2026-04-14 21:30:45
================================================================================

🔑 ============================================================================
   KEY EXCHANGE METHOD DETECTED:
   ────────────────────────────────────────────────────────────────────────────
   🔐 CLASSICAL MODE: X25519
   └─ Algorithm: Elliptic Curve Diffie-Hellman
   Security: ⭐ MEDIUM (Vulnerable to Quantum)
================================================================================

🔐 ============================================================================
   CIPHER SUITE:
   ────────────────────────────────────────────────────────────────────────────
   TLS_AES_256_GCM_SHA384
================================================================================

📡 ============================================================================
   PROTOCOL VERSION:
   ────────────────────────────────────────────────────────────────────────────
   TLSv1.3
================================================================================

💬 ============================================================================
   MESSAGE RECEIVED (DECRYPTED):
   ────────────────────────────────────────────────────────────────────────────
   >>> Hi, how are you <<<
================================================================================

✅ ============================================================================
   TLS HANDSHAKE COMPLETED SUCCESSFULLY
================================================================================
```

---

## **Method 2: Verbose Shell Script**

**On Mac:**
```bash
cd ~/Desktop/"Gagan NS prjt"
./scripts/start_server_verbose.sh
```

---

## **Method 3: Check Dashboard (Kali)**

After clicking buttons, check the **TLS Details** panel:

```
🔐 TLS Handshake Details
─────────────────────────
Version:      TLSv1.3
Cipher:       TLS_AES_256_GCM_SHA384
Key Exchange: X25519              ← THIS SHOWS THE MODE!
```

---

## **Comparison Table:**

| Mode | Key Exchange | Packet Size | Security |
|------|-------------|-------------|----------|
| **RSA** | X25519 | ~2-3 KB | ⭐ Medium (Quantum-vulnerable) |
| **PQC** | MLKEM768 | ~4-5 KB | ⭐⭐ High (Quantum-safe) |
| **Hybrid** | X25519MLKEM768 | ~5-6 KB | ⭐⭐⭐ Maximum (Both) |

---

## **Quick Test:**

### **Terminal 1 (Mac):**
```bash
python3 tls_server_enhanced.py
```

### **Terminal 2 (Kali):**
Open browser: http://localhost:5000

1. Click **RSA** → See "X25519" on Mac
2. Click **PQC** → See "MLKEM768" on Mac
3. Click **Hybrid** → See "X25519MLKEM768" on Mac

Each time you'll see:
- ✅ Key exchange method
- ✅ Cipher suite
- ✅ Message: "Hi, how are you"
- ✅ Security level

---

## **Example Output for Each Mode:**

### **RSA Mode:**
```
🔑 KEY EXCHANGE METHOD DETECTED:
   🔐 CLASSICAL MODE: X25519
   └─ Algorithm: Elliptic Curve Diffie-Hellman
   Security: ⭐ MEDIUM (Vulnerable to Quantum)

💬 MESSAGE RECEIVED (DECRYPTED):
   >>> Hi, how are you <<<
```

### **PQC Mode:**
```
🔑 KEY EXCHANGE METHOD DETECTED:
   🛡️  POST-QUANTUM MODE: MLKEM768
   └─ Algorithm: Kyber (NIST PQC Standard)
   Security: ⭐⭐ HIGH (Quantum-Resistant)

💬 MESSAGE RECEIVED (DECRYPTED):
   >>> Hi, how are you <<<
```

### **Hybrid Mode:**
```
🔑 KEY EXCHANGE METHOD DETECTED:
   🔥 HYBRID MODE: X25519 + MLKEM768
   ├─ Classical: X25519 (Elliptic Curve)
   └─ Post-Quantum: MLKEM768 (Kyber)
   Security: ⭐⭐⭐ MAXIMUM (Quantum-Resistant)

💬 MESSAGE RECEIVED (DECRYPTED):
   >>> Hi, how are you <<<
```

---

## **Troubleshooting:**

### Can't see message?
The message is encrypted during transmission. The server decrypts it automatically.

### Want to see raw encrypted data?
Add `-debug` flag:
```bash
python3 tls_server_enhanced.py -debug
```

### Want to capture with Wireshark?
```bash
# Terminal 1
sudo tcpdump -i any -w tls_capture.pcap port 4433

# Terminal 2
python3 tls_server_enhanced.py

# Click buttons on Kali

# Stop tcpdump (Ctrl+C), then analyze
wireshark tls_capture.pcap
```

---

**Now you can clearly see:**
✅ Which encryption mode is being used  
✅ The message being sent  
✅ Security level of each mode  
✅ Packet sizes and performance  
