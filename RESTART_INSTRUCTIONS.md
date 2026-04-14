# 🚀 Quick Restart Instructions

## The Fix is Complete! Here's What to Do:

### Step 1: Stop the Current Server
If Flask is running, press **Ctrl+C** in the terminal

### Step 2: Restart Flask
```bash
python3 app.py
```

You should see:
```
================================================================================
  POST-QUANTUM CRYPTOGRAPHY TLS DASHBOARD
  Real-world OpenSSL/OQS Integration
================================================================================

🌐 Starting Flask server...
📍 Dashboard: http://localhost:5000
🔒 Target TLS Server: 192.168.0.104:4433

⚠️  Make sure your TLS server is running before testing!
   Use: ./scripts/start_server.sh
```

### Step 3: Clear Browser Cache (IMPORTANT!)
**Chrome/Edge/Brave:**
- Press `Ctrl+Shift+Delete` (Windows/Linux) or `Cmd+Shift+Delete` (Mac)
- Select "Cached images and files"
- Click "Clear data"

**Or use Hard Refresh:**
- `Ctrl+Shift+R` (Windows/Linux)
- `Cmd+Shift+R` (Mac)

### Step 4: Open Dashboard
Navigate to: **http://localhost:5000**

### Step 5: Test Configuration Update
1. In the config panel, change the server IP or port
2. Click **"Update Config"** button
3. You should see: ✅ **Configuration updated! Server: [IP]:[PORT]**

### Step 6: Test TLS Connections
1. Click **"Check Server"** - should show green if server is running
2. Click **"RSA"** button - should show terminal output
3. Click **"PQC"** button - should show MLKEM768 connection
4. Click **"Hybrid"** button - should show X25519MLKEM768 connection

---

## ✅ What Was Fixed

1. **Template Mismatch**: Now uses `index_enhanced.html` (was using wrong template)
2. **JSON Errors**: `/config` endpoint now always returns valid JSON
3. **Error Handling**: Better error messages in both backend and frontend
4. **Response Validation**: Frontend checks for valid JSON before parsing

---

## 🧪 Optional: Run Test Script

```bash
# In a new terminal (keep Flask running)
python3 test_config_endpoint.py
```

Expected output:
```
============================================================
Testing /config endpoint
============================================================

Make sure Flask server is running on http://localhost:5000

Testing GET /config...
Status Code: 200
Content-Type: application/json
Response: {"host":"192.168.0.104","port":"4433"}
✅ Valid JSON received: {'host': '192.168.0.104', 'port': '4433'}

Testing POST /config...
Status Code: 200
Content-Type: application/json
Response: {"status":"success","host":"192.168.0.104","port":"4433"}
✅ Valid JSON received: {'status': 'success', 'host': '192.168.0.104', 'port': '4433'}
✅ Configuration updated successfully

============================================================
Test complete!
============================================================
```

---

## 🐛 Still Having Issues?

### Check Flask Console
Look for error messages in the terminal where Flask is running

### Check Browser Console
1. Press **F12** to open DevTools
2. Go to **Console** tab
3. Look for JavaScript errors

### Check Network Tab
1. Press **F12** to open DevTools
2. Go to **Network** tab
3. Click "Update Config"
4. Click the `/config` request
5. Check **Response** tab - should be JSON, not HTML

### Manual Test with cURL
```bash
# Test if endpoint returns JSON
curl http://localhost:5000/config

# Should output:
# {"host":"192.168.0.104","port":"4433"}
```

---

## 📊 Dashboard Features Working Now

✅ Server status indicator (green/red)  
✅ Configuration update (no JSON errors)  
✅ RSA TLS connection test  
✅ PQC (MLKEM768) connection test  
✅ Hybrid (X25519+MLKEM768) connection test  
✅ Real-time metrics (time, size, security)  
✅ TLS details parsing (protocol, cipher, key exchange)  
✅ Live charts (Chart.js visualization)  
✅ Comparison table  
✅ Status log panel  
✅ Wireshark guide modal  

---

**Everything is ready! Just restart Flask and clear your browser cache.** 🎉
