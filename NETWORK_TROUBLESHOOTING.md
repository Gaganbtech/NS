# 🌐 Network Troubleshooting for Kali

## Problem
`fatal: unable to access 'https://github.com/Gaganbtech/NS.git/': Could not resolve host: github.com`

This means your Kali machine cannot resolve DNS or reach GitHub.

---

## Solution 1: Check Internet Connection

```bash
# Test internet connectivity
ping -c 4 8.8.8.8

# Test DNS resolution
ping -c 4 google.com

# Test GitHub specifically
ping -c 4 github.com
```

**If ping to 8.8.8.8 works but github.com doesn't**, it's a DNS issue.

---

## Solution 2: Fix DNS Resolution

### Method A: Use Google DNS
```bash
# Edit resolv.conf
sudo nano /etc/resolv.conf

# Add these lines at the top:
nameserver 8.8.8.8
nameserver 8.8.4.4

# Save and exit (Ctrl+X, Y, Enter)

# Test
ping github.com
```

### Method B: Restart Network Service
```bash
# Restart networking
sudo systemctl restart NetworkManager

# Or
sudo service network-manager restart

# Test again
ping github.com
```

### Method C: Flush DNS Cache
```bash
# Flush DNS cache
sudo systemd-resolve --flush-caches

# Or
sudo /etc/init.d/dns-clean restart

# Test
ping github.com
```

---

## Solution 3: Check Firewall

```bash
# Check if firewall is blocking
sudo iptables -L

# Temporarily disable firewall to test
sudo ufw disable

# Try git clone again
git clone https://github.com/Gaganbtech/NS.git

# Re-enable firewall after
sudo ufw enable
```

---

## Solution 4: Use Different Network

If you're on a restricted network (corporate, school, etc.):

1. **Try mobile hotspot** - Connect Kali to your phone's hotspot
2. **Try different WiFi** - Switch to a different network
3. **Use VPN** - If GitHub is blocked in your region

---

## Solution 5: Transfer Files Directly (Bypass GitHub)

Since you have the files on your Mac, you can transfer them directly to Kali:

### Method A: Using SCP (Secure Copy)
```bash
# On Kali, find your IP
ip addr show

# On Mac, transfer the entire project
cd ~/Desktop
scp -r "Gagan NS prjt" gagan@[KALI_IP]:~/NS

# Example:
# scp -r "Gagan NS prjt" gagan@192.168.1.100:~/NS
```

### Method B: Using USB Drive
```bash
# On Mac: Copy project to USB drive
# On Kali: Mount USB and copy files
sudo mkdir /mnt/usb
sudo mount /dev/sdb1 /mnt/usb
cp -r /mnt/usb/NS ~/NS
```

### Method C: Using Shared Folder (VirtualBox/VMware)
If Kali is a VM:
1. Set up shared folder in VM settings
2. Copy files to shared folder from Mac
3. Access from Kali

### Method D: Using Python HTTP Server
```bash
# On Mac (in project directory):
cd ~/Desktop/"Gagan NS prjt"
python3 -m http.server 8000

# On Kali:
wget -r -np -nH --cut-dirs=0 http://[MAC_IP]:8000/
# Or use browser: http://[MAC_IP]:8000
```

### Method E: Create ZIP and Transfer
```bash
# On Mac:
cd ~/Desktop
zip -r NS.zip "Gagan NS prjt"

# Transfer via any method (email, cloud, USB, etc.)

# On Kali:
unzip NS.zip
mv "Gagan NS prjt" NS
cd NS
```

---

## Solution 6: Use Git with Different Protocol

```bash
# Try SSH instead of HTTPS
git clone git@github.com:Gaganbtech/NS.git

# Or try with explicit DNS
git clone https://140.82.121.4/Gaganbtech/NS.git
```

---

## Quick Diagnostic Commands

```bash
# 1. Check network interface
ip link show

# 2. Check IP address
ip addr show

# 3. Check default gateway
ip route show

# 4. Check DNS servers
cat /etc/resolv.conf

# 5. Test DNS resolution
nslookup github.com

# 6. Test with different DNS
nslookup github.com 8.8.8.8

# 7. Check if GitHub is reachable
curl -I https://github.com

# 8. Trace route to GitHub
traceroute github.com
```

---

## Recommended: Direct File Transfer via SCP

Since you have both machines, this is the fastest solution:

### Step-by-Step:

#### On Kali:
```bash
# 1. Install SSH server (if not installed)
sudo apt update
sudo apt install openssh-server -y

# 2. Start SSH service
sudo systemctl start ssh

# 3. Find your Kali IP
ip addr show
# Look for inet 192.168.x.x

# 4. Note your username
whoami
```

#### On Mac:
```bash
# Navigate to project directory
cd ~/Desktop

# Transfer entire project to Kali
scp -r "Gagan NS prjt" gagan@[KALI_IP]:~/NS

# Example:
# scp -r "Gagan NS prjt" gagan@192.168.1.100:~/NS

# Enter Kali password when prompted
```

#### Back on Kali:
```bash
# Verify files are there
cd ~/NS
ls -la

# Run the dashboard
python3 app.py
```

---

## Alternative: Use Cloud Storage

### Upload from Mac:
1. Compress the project: `zip -r NS.zip "Gagan NS prjt"`
2. Upload to Google Drive / Dropbox / OneDrive
3. Get shareable link

### Download on Kali:
```bash
# For Google Drive (using gdown)
pip3 install gdown
gdown [GOOGLE_DRIVE_FILE_ID]

# Or use browser to download
# Then unzip
unzip NS.zip
```

---

## Once Network is Fixed

```bash
# Test GitHub access
ping github.com

# Clone repository
git clone https://github.com/Gaganbtech/NS.git

# Enter directory
cd NS

# Install dependencies
pip3 install flask

# Run dashboard
python3 app.py
```

---

## Summary of Best Options

1. **Fastest**: SCP transfer from Mac to Kali (if on same network)
2. **Most Reliable**: Fix DNS by adding Google DNS (8.8.8.8)
3. **Easiest**: Use mobile hotspot to bypass network restrictions
4. **Offline**: USB drive transfer

Choose the method that works best for your situation!
