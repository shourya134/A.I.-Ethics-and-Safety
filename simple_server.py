#!/usr/bin/env python3
"""
Super simple web server for hosting results - no fancy features
"""

import http.server
import socketserver
import webbrowser
import os
import threading
import time

def start_simple_server():
    """Start the simplest possible web server"""
    
    PORT = 8000
    
    # Try to find an available port
    for port in range(8000, 8010):
        try:
            with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
                PORT = port
                break
        except OSError:
            continue
    else:
        print("Could not find available port")
        return
    
    # Change to directory with results
    if os.path.exists("demo_plots"):
        os.chdir("demo_plots")
        print(f"Serving demo_plots directory")
    else:
        print("Serving current directory (demo_plots not found)")
    
    print(f"Starting server on port {PORT}")
    print(f"Open your browser to: http://localhost:{PORT}")
    print("Press Ctrl+C to stop")
    
    # Start server
    try:
        with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
            # Open browser after short delay
            def open_browser():
                time.sleep(1)
                try:
                    webbrowser.open(f"http://localhost:{PORT}")
                    print("Browser opened")
                except:
                    print("Could not open browser automatically")
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            # Serve forever
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    start_simple_server()