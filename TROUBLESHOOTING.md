# 🔧 Troubleshooting Guide - Local Server

## ❌ Common Issues & Solutions

### **Issue: "Python is not recognized"**
```bash
# Try these commands:
python simple_server.py
python3 simple_server.py
py simple_server.py
```

### **Issue: "Port already in use"**
```bash
# Check what's using port 8000:
netstat -ano | findstr :8000

# Kill the process (replace PID):
taskkill /PID <PID> /F

# Or use our auto-port detection
```

### **Issue: "No module named..."**
The simple server only uses built-in Python modules, so this shouldn't happen.

### **Issue: "Permission denied"**
```bash
# Run as administrator or try different port:
python simple_server.py
```

## ✅ Working Solutions

### **Method 1: Super Simple (Recommended)**
```bash
# Double-click this file:
run_server.bat

# Or run manually:
python simple_server.py
```

### **Method 2: Basic Python Server**
```bash
# Navigate to demo_plots folder
cd demo_plots

# Start Python's built-in server
python -m http.server 8000

# Open browser to: http://localhost:8000
```

### **Method 3: Manual File Opening**
If the server doesn't work, you can open the HTML files directly:
1. Navigate to `demo_plots` folder
2. Double-click `index.html`
3. Or open `dashboard/overview_dashboard.html` directly

## 🧪 Test Steps

### 1. **Test Python**
```bash
python --version
# Should show: Python 3.x.x
```

### 2. **Test Simple Server**
```bash
python simple_server.py
# Should show: "Starting server on port 8000"
```

### 3. **Test URL**
Open browser to: `http://localhost:8000`

### 4. **Test Files**
You should see:
- `index.html` - Main demo page
- `dashboard/` - Interactive charts
- `data/` - JSON data files

## 🔍 Debug Information

### **Check Files Exist**
```bash
dir demo_plots
# Should show: dashboard, data, index.html
```

### **Check Port Availability**
```bash
netstat -an | findstr :8000
# Should show nothing if port is free
```

### **Manual URL Test**
Try these URLs in your browser:
- `http://localhost:8000`
- `http://localhost:8000/index.html`
- `http://localhost:8000/dashboard/overview_dashboard.html`

## 🆘 If Nothing Works

### **Option 1: Direct File Access**
```bash
# Open HTML files directly in browser
start demo_plots\index.html
start demo_plots\dashboard\overview_dashboard.html
```

### **Option 2: Alternative Ports**
```bash
# Try different ports manually
python -m http.server 8001
python -m http.server 8080
python -m http.server 3000
```

### **Option 3: File Explorer**
1. Open File Explorer
2. Navigate to your project folder
3. Go to `demo_plots` folder
4. Double-click `index.html`

## 📋 Quick Diagnostics

Run these commands and tell me the results:

```bash
# Check Python
python --version

# Check files
dir demo_plots

# Check if port is free
netstat -an | findstr :8000

# Try basic server
python -m http.server 8000
```

## 🎯 What Should Work

The `simple_server.py` uses only basic Python features:
- ✅ No external dependencies
- ✅ Auto-finds available ports
- ✅ Opens browser automatically
- ✅ Works with any Python 3.x

## 💡 Alternative Viewing Methods

### **Method A: Browser File Protocol**
Open browser and navigate to:
```
file:///C:/Users/shour/A.I.-Ethics-and-Safety/demo_plots/index.html
```

### **Method B: Local File Manager**
1. Open Windows Explorer
2. Navigate to your project
3. Open `demo_plots` folder
4. Double-click any `.html` file

### **Method C: VS Code Live Server**
If you have VS Code:
1. Install "Live Server" extension
2. Right-click on `index.html`
3. Select "Open with Live Server"

---

## 🚨 Emergency Instructions

If NOTHING works, here's the manual process:

1. **Open File Explorer**
2. **Go to:** `C:\Users\shour\A.I.-Ethics-and-Safety\demo_plots`
3. **Double-click:** `index.html`
4. **This will open in your default browser**
5. **Click the links to see different visualizations**

The HTML files contain all the interactive charts and work without a server!