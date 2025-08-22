#!/usr/bin/env python3
"""
Quick deployment script for jailbreak detection results
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def run_command(command, description):
    """Run a command and show progress"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed!")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def check_requirements():
    """Check if required files exist"""
    required_files = [
        "scripts/visualize_results.py",
        "scripts/serve_results.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    return missing_files

def main():
    print("🛡️  AI SAFETY JAILBREAK DETECTION - QUICK DEPLOY")
    print("=" * 55)
    
    # Check requirements
    missing = check_requirements()
    if missing:
        print("❌ Missing required files:")
        for file in missing:
            print(f"   - {file}")
        print("💡 Make sure you're in the project root directory")
        return
    
    # Step 1: Generate demo results
    print("📊 Step 1: Generating visualization results...")
    if not run_command("python scripts/visualize_results.py --demo --output-dir demo_plots", 
                      "Generating demo visualizations"):
        print("💡 Trying alternative Python command...")
        if not run_command("python3 scripts/visualize_results.py --demo --output-dir demo_plots", 
                          "Generating demo visualizations (python3)"):
            print("❌ Could not generate visualizations")
            print("💡 Try running manually: python scripts/visualize_results.py --demo")
            return
    
    # Step 2: Start local server
    print("\n🌐 Step 2: Starting local web server...")
    print("🚀 Your results will be available at: http://localhost:8000")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 55)
    
    try:
        # Start server (this will block)
        subprocess.run([sys.executable, "scripts/serve_results.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except subprocess.CalledProcessError:
        print("❌ Failed to start server")
        print("💡 Try running manually: python scripts/serve_results.py")

if __name__ == "__main__":
    main()