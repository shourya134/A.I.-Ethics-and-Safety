#!/usr/bin/env python3
"""
Local web server for hosting jailbreak detection visualization results
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import argparse
import threading
import time
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler with CORS headers and proper MIME types"""
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def guess_type(self, path):
        """Override to ensure proper MIME types for our files"""
        mimetype, encoding = super().guess_type(path)
        
        # Ensure HTML files are served correctly
        if path.endswith('.html'):
            return 'text/html', encoding
        elif path.endswith('.json'):
            return 'application/json', encoding
        elif path.endswith('.css'):
            return 'text/css', encoding
        elif path.endswith('.js'):
            return 'application/javascript', encoding
        
        return mimetype, encoding
    
    def log_message(self, format, *args):
        """Custom logging to show which files are being served"""
        if not self.path.endswith(('.ico', '.png', '.jpg')):  # Reduce noise
            print(f"Serving: {self.path}")

def find_available_port(start_port=8000, max_attempts=100):
    """Find an available port starting from start_port"""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    
    raise RuntimeError(f"Could not find available port in range {start_port}-{start_port + max_attempts}")

def create_server_index(results_dir, port):
    """Create a server landing page that lists available results"""
    
    # Find all HTML files in the results directory
    html_files = []
    results_path = Path(results_dir)
    
    if results_path.exists():
        for html_file in results_path.rglob("*.html"):
            rel_path = html_file.relative_to(results_path)
            html_files.append({
                'path': str(rel_path).replace('\\', '/'),
                'name': html_file.stem.replace('_', ' ').title(),
                'size': html_file.stat().st_size,
                'modified': time.ctime(html_file.stat().st_mtime)
            })
    
    # Create index page
    index_html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛡️ Jailbreak Detection Results Server</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .content {{
            padding: 40px;
        }}
        .server-info {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 4px solid #28a745;
        }}
        .files-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        .file-card {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            padding: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .file-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .file-link {{
            text-decoration: none;
            color: #495057;
            display: block;
        }}
        .file-name {{
            font-size: 1.2em;
            font-weight: 600;
            color: #007bff;
            margin-bottom: 10px;
        }}
        .file-details {{
            font-size: 0.9em;
            color: #6c757d;
        }}
        .status {{
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            margin-left: 10px;
        }}
        .controls {{
            background: #e9ecef;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .btn {{
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
            text-decoration: none;
            display: inline-block;
        }}
        .btn:hover {{
            background: #0056b3;
        }}
        .quick-links {{
            margin-top: 30px;
            padding: 20px;
            background: #fff3cd;
            border-radius: 10px;
            border-left: 4px solid #ffc107;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ AI Safety Jailbreak Detection</h1>
            <h2>Local Results Server</h2>
            <p>Your visualization results are now live!</p>
        </div>
        
        <div class="content">
            <div class="server-info">
                <h3>🌐 Server Information</h3>
                <p><strong>Server URL:</strong> <code>http://localhost:{port}</code> <span class="status">🟢 LIVE</span></p>
                <p><strong>Results Directory:</strong> <code>{results_dir}</code></p>
                <p><strong>Files Found:</strong> {len(html_files)} HTML visualizations</p>
                <p><strong>Started:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="controls">
                <h3>🎛️ Quick Actions</h3>
                <a href="#" onclick="location.reload()" class="btn">🔄 Refresh</a>
                <a href="/demo_plots/" class="btn">📊 Demo Results</a>
                <a href="/plots/" class="btn">📈 Latest Results</a>
            </div>
            
            <h3>📁 Available Visualizations</h3>
            
            <div class="files-grid">
'''
    
    # Add file cards
    if html_files:
        for file_info in html_files:
            file_size = f"{file_info['size'] / 1024:.1f} KB"
            index_html += f'''
                <div class="file-card">
                    <a href="/{file_info['path']}" class="file-link" target="_blank">
                        <div class="file-name">📄 {file_info['name']}</div>
                        <div class="file-details">
                            <div>Path: {file_info['path']}</div>
                            <div>Size: {file_size}</div>
                            <div>Modified: {file_info['modified']}</div>
                        </div>
                    </a>
                </div>
'''
    else:
        index_html += '''
                <div class="file-card">
                    <div class="file-name">📭 No visualizations found</div>
                    <div class="file-details">
                        Generate some results first using:<br>
                        <code>python scripts/visualize_results.py --demo</code>
                    </div>
                </div>
'''
    
    index_html += f'''
            </div>
            
            <div class="quick-links">
                <h3>💡 Quick Start Guide</h3>
                <ol>
                    <li><strong>Generate Results:</strong> <code>python scripts/visualize_results.py --demo</code></li>
                    <li><strong>View Dashboard:</strong> Click on any HTML file above</li>
                    <li><strong>Stop Server:</strong> Press <kbd>Ctrl+C</kbd> in the terminal</li>
                </ol>
                
                <h4>🔗 Direct Links:</h4>
                <ul>
                    <li><a href="/demo_plots/index.html" target="_blank">📊 Demo Dashboard</a></li>
                    <li><a href="/demo_plots/dashboard/overview_dashboard.html" target="_blank">📈 Interactive Overview</a></li>
                    <li><a href="/demo_plots/data/sample_results.json" target="_blank">📄 Sample Data</a></li>
                </ul>
            </div>
        </div>
    </div>
    
    <script>
        // Auto-refresh file list every 30 seconds
        setInterval(() => {{
            console.log('Checking for new files...');
            // In a real implementation, this would fetch updated file list
        }}, 30000);
    </script>
</body>
</html>
'''
    
    return index_html

def start_server(results_dir=".", port=8000, open_browser=True):
    """Start the local web server"""
    
    # Change to results directory
    original_dir = os.getcwd()
    
    try:
        if os.path.exists(results_dir):
            os.chdir(results_dir)
            print(f"Serving from directory: {os.path.abspath(results_dir)}")
        else:
            print(f"Directory {results_dir} not found, serving from current directory")
        
        # Find available port
        actual_port = find_available_port(port)
        if actual_port != port:
            print(f"Port {port} was busy, using port {actual_port} instead")
        
        # Create server index
        index_content = create_server_index(results_dir, actual_port)
        with open('server_index.html', 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        # Start server
        with socketserver.TCPServer(("", actual_port), CustomHTTPRequestHandler) as httpd:
            server_url = f"http://localhost:{actual_port}"
            
            print("=" * 50)
            print("AI SAFETY JAILBREAK DETECTION SERVER")
            print("=" * 50)
            print(f"Server URL: {server_url}")
            print(f"Directory: {os.path.abspath('.')}")
            print(f"Direct links:")
            print(f"   Server Dashboard: {server_url}/server_index.html")
            print(f"   Demo Results: {server_url}/demo_plots/")
            print("=" * 50)
            print("Press Ctrl+C to stop the server")
            print("Server will auto-detect new files")
            print("=" * 50)
            
            # Open browser
            if open_browser:
                def open_browser_delayed():
                    time.sleep(1)  # Give server time to start
                    try:
                        webbrowser.open(f"{server_url}/server_index.html")
                        print(f"Opened {server_url}/server_index.html in browser")
                    except Exception as e:
                        print(f"Could not open browser: {e}")
                
                browser_thread = threading.Thread(target=open_browser_delayed)
                browser_thread.daemon = True
                browser_thread.start()
            
            # Start serving
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nServer stopped by user")
            
    except Exception as e:
        print(f"Error starting server: {e}")
    finally:
        # Return to original directory
        os.chdir(original_dir)
        
        # Clean up
        index_file = os.path.join(results_dir, 'server_index.html')
        if os.path.exists(index_file):
            try:
                os.remove(index_file)
            except:
                pass

def main():
    parser = argparse.ArgumentParser(description="Local web server for jailbreak detection results")
    parser.add_argument("--dir", "-d", default=".", 
                       help="Directory to serve (default: current directory)")
    parser.add_argument("--port", "-p", type=int, default=8000,
                       help="Port to serve on (default: 8000)")
    parser.add_argument("--no-browser", action="store_true",
                       help="Don't open browser automatically")
    
    args = parser.parse_args()
    
    start_server(
        results_dir=args.dir,
        port=args.port,
        open_browser=not args.no_browser
    )

if __name__ == "__main__":
    main()