# 🚀 Quick Transfer Guide: Mac → Kali (SCP Method)

Since GitHub is not accessible from your Kali machine, let's transfer files directly!

---

## 📋 Prerequisites

- Mac and Kali on the same network (WiFi/Ethernet)
- SSH enabled on Kali

---

## 🔧 Step 1: Setup Kali (Run on Kali)

```bash
# Install SSH server
sudo apt update
sudo apt install openssh-server -y

# Start SSH service
sudo systemctl start ssh
sudo systemctl enable ssh

# Check SSH is running
sudo systemctl status ssh

# Find your Kali IP address
ip addr show
# Look for: inet 192.168.x.x (e.g., 192.168.1.100)

# Note your username
whoami
# Usually: gagan
```

**Write down your Kali IP**: `192.168.___.___ `

---

## 📤 Step 2: Transfer from Mac (Run on Mac)

```bash
# Navigate to project parent directory
cd ~/Desktop

# Transfer entire project to Kali
# Replace [KALI_IP] with the IP you noted above
scp -r "Gagan NS prjt" gagan@[KALI_IP]:~/NS

# Example:
# scp -r "Gagan NS prjt" gagan@192.168.1.100:~/NS
```

**You'll be prompted for Kali password** - enter it.

### Expected Output:
```
app.py                    100%   15KB   1.2MB/s   00:00
index_enhanced.html       100%   12KB   1.5MB/s   00:00
script_enhanced.js        100%   18KB   2.1MB/s   00:00
...
[Progress bar showing file transfer]
```

---

## ✅ Step 3: Verify on Kali (Run on Kali)

```bash
# Check files are there
cd ~/NS
ls -la

# You should see:
# app.py
# templates/
# static/
# scripts/
# etc.
```

---

## 🚀 Step 4: Run Dashboard (Run on Kali)

```bash
# Install Flask
pip3 install flask

# Run the dashboard
python3 app.py
```

**Dashboard will be available at**: http://localhost:5000

---

## 🔥 One-Line Commands

### On Kali:
```bash
sudo apt install openssh-server -y && sudo systemctl start ssh && ip addr show | grep "inet "
```

### On Mac (replace KALI_IP):
```bash
cd ~/Desktop && scp -r "Gagan NS prjt" gagan@KALI_IP:~/NS
```

### On Kali (after transfer):
```bash
cd ~/NS && pip3 install flask && python3 app.py
```

---

## 🐛 Troubleshooting

### "Connection refused"
```bash
# On Kali, make sure SSH is running
sudo systemctl start ssh
sudo systemctl status ssh
```

### "Permission denied"
```bash
# Make sure you're using correct username
# Check with: whoami (on Kali)
```

### "No route to host"
```bash
# Make sure both machines are on same network
# On Mac: ifconfig | grep "inet "
# On Kali: ip addr show | grep "inet "
# They should be in same subnet (e.g., 192.168.1.x)
```

### "Host key verification failed"
```bash
# On Mac, remove old key
ssh-keygen -R [KALI_IP]
# Then try scp again
```

---

## 🎯 Alternative: Use SFTP (GUI Method)

If you prefer a GUI:

### On Mac:
1. Open **Finder**
2. Press **Cmd+K**
3. Enter: `sftp://gagan@[KALI_IP]`
4. Enter Kali password
5. Drag and drop the project folder

### Or use FileZilla:
1. Download FileZilla (free)
2. Host: `sftp://[KALI_IP]`
3. Username: `gagan`
4. Password: [your Kali password]
5. Port: `22`
6. Drag and drop files

---

## 📦 Alternative: Create Archive First

If transfer is slow, compress first:

### On Mac:
```bash
cd ~/Desktop
tar -czf NS.tar.gz "Gagan NS prjt"
scp NS.tar.gz gagan@[KALI_IP]:~/
```

### On Kali:
```bash
cd ~
tar -xzf NS.tar.gz
mv "Gagan NS prjt" NS
cd NS
python3 app.py
```

---

## ⚡ Super Fast Method (Python HTTP Server)

### On Mac:
```bash
cd ~/Desktop/"Gagan NS prjt"
python3 -m http.server 8000

# Note your Mac IP
ifconfig | grep "inet "
```

### On Kali:
```bash
# Download entire project
wget -r -np -nH --cut-dirs=0 -R "index.html*" http://[MAC_IP]:8000/

# Or just download as zip
# (First create zip on Mac)
wget http://[MAC_IP]:8000/NS.zip
unzip NS.zip
```

---

## ✅ Verification Checklist

After transfer, verify these files exist on Kali:

```bash
cd ~/NS

# Check main files
ls -la app.py
ls -la requirements.txt
ls -la templates/index_enhanced.html
ls -la static/script_enhanced.js
ls -la static/style.css

# Check scripts
ls -la scripts/*.sh

# Check docs
ls -la *.md
```

All should show file sizes, not "No such file or directory"

---

## 🎉 Success!

Once files are transferred:

```bash
cd ~/NS
python3 app.py
```

Open browser: **http://localhost:5000**

---

## 📝 Quick Reference

| Task | Command |
|------|---------|
| Start SSH on Kali | `sudo systemctl start ssh` |
| Find Kali IP | `ip addr show` |
| Transfer from Mac | `scp -r "Gagan NS prjt" gagan@KALI_IP:~/NS` |
| Verify on Kali | `cd ~/NS && ls -la` |
| Run dashboard | `python3 app.py` |

---

**Estimated Transfer Time**: 1-2 minutes (depending on network speed)

**Total Setup Time**: 5 minutes

**Status**: ✅ Ready to transfer!
