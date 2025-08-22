# 🚀 Deployment Guide - AI Safety Jailbreak Detection

## 🌐 Local Hosting (Recommended)

### Quick Start (One Command)

```bash
# Windows
deploy.bat

# Linux/Mac/Windows with Python
python deploy.py
```

### Manual Steps

1. **Generate Results:**
   ```bash
   python scripts/visualize_results.py --demo --output-dir demo_plots
   ```

2. **Start Local Server:**
   ```bash
   python scripts/serve_results.py
   ```

3. **Open Browser:**
   Navigate to `http://localhost:8000`

## 📊 Server Features

### 🎯 **Auto-Detection**
- Automatically finds available ports (8000, 8001, 8002...)
- Scans for HTML files in your results directory
- Creates dynamic landing page with file listings

### 🔄 **Live Updates**
- Server detects new visualization files
- Auto-refresh capabilities
- Real-time file monitoring

### 🌐 **Web Interface**
- Professional server dashboard
- File browser with metadata
- Direct links to all visualizations
- Mobile-responsive design

## 📂 Directory Structure

```
your-project/
├── demo_plots/                 # Generated demo results
│   ├── index.html             # Main demo page
│   ├── dashboard/
│   │   └── overview_dashboard.html
│   └── data/
│       └── sample_results.json
├── plots/                     # Your actual results
│   ├── dashboard/
│   ├── metrics/
│   └── comparisons/
└── scripts/
    ├── visualize_results.py   # Generate visualizations
    └── serve_results.py       # Local web server
```

## 🎛️ Server Configuration

### Command Line Options

```bash
# Basic usage
python scripts/serve_results.py

# Custom directory
python scripts/serve_results.py --dir ./my_results

# Custom port
python scripts/serve_results.py --port 8080

# Don't open browser automatically
python scripts/serve_results.py --no-browser
```

### Environment Variables

```bash
# Set default port
export JAILBREAK_SERVER_PORT=8080

# Set default directory
export JAILBREAK_RESULTS_DIR=./results
```

## 🔗 URL Structure

| URL | Description |
|-----|-------------|
| `http://localhost:8000/` | Server dashboard |
| `http://localhost:8000/demo_plots/` | Demo visualizations |
| `http://localhost:8000/plots/` | Your results |
| `http://localhost:8000/dashboard/overview_dashboard.html` | Main dashboard |

## 🎨 Customization

### Custom Styling

Edit the server template in `scripts/serve_results.py`:

```python
# Find this section and modify CSS
.header {
    background: linear-gradient(45deg, #your-colors);
    # ... your custom styles
}
```

### Custom Landing Page

Create `custom_index.html` in your results directory to override the default landing page.

## 🔧 Troubleshooting

### Port Already in Use
```bash
# The server automatically finds available ports
# Or manually specify:
python scripts/serve_results.py --port 8001
```

### Python Command Not Found
```bash
# Try alternative Python commands:
python3 scripts/serve_results.py
py scripts/serve_results.py
```

### No Visualizations Found
```bash
# Generate demo data first:
python scripts/visualize_results.py --demo

# Or use your own results:
python scripts/visualize_results.py --results-file your_results.json
```

### Browser Doesn't Open
```bash
# Start server without auto-browser:
python scripts/serve_results.py --no-browser

# Then manually open: http://localhost:8000
```

## 📱 Mobile Access

The server is accessible from mobile devices on the same network:

1. **Find your computer's IP address:**
   ```bash
   # Windows
   ipconfig
   
   # Linux/Mac
   ifconfig
   ```

2. **Access from mobile:**
   ```
   http://YOUR_IP_ADDRESS:8000
   ```

## 🔒 Security Notes

### Local Development Only
- The server is designed for local development
- No authentication or security features
- Do not expose to the internet directly

### Firewall Considerations
- Server runs on localhost by default
- Windows may ask for firewall permission
- Safe for local network access

## 🚀 Production Deployment

For production deployment, consider:

### Static File Hosting
```bash
# Copy files to web server
cp -r demo_plots/* /var/www/html/

# Or use cloud storage
aws s3 sync demo_plots/ s3://your-bucket/results/
```

### Docker Container
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
EXPOSE 8000
CMD ["python", "scripts/serve_results.py", "--port", "8000"]
```

### GitHub Pages
```bash
# Push to gh-pages branch
git checkout --orphan gh-pages
git add demo_plots/*
git commit -m "Deploy visualizations"
git push origin gh-pages
```

## 📊 Performance Tips

### Large Datasets
- Use `--head-limit` in visualization generation
- Split results into multiple pages
- Consider data sampling for overview

### File Size Optimization
- Compress PNG images
- Minify HTML/CSS/JS
- Use CDN for external libraries

## 🆘 Support

### Common Issues

| Issue | Solution |
|-------|----------|
| "Port 8000 in use" | Server auto-finds available port |
| "No Python found" | Install Python or use `python3` |
| "No files found" | Run visualization script first |
| "Browser won't open" | Manually go to `localhost:8000` |

### Getting Help

1. **Check the logs** - Server shows detailed output
2. **Try demo mode** - `python scripts/visualize_results.py --demo`
3. **Verify file structure** - Ensure scripts are in correct location
4. **Test manually** - Run each step individually

---

## 🎉 You're All Set!

Your AI Safety Jailbreak Detection results are now deployed locally! 

🌐 **Access URL:** `http://localhost:8000`
📊 **Features:** Interactive dashboards, real-time updates, mobile support
🔄 **Updates:** Re-run visualization scripts to refresh data

Happy analyzing! 🛡️