#!/usr/bin/env python3
"""
BETTING PRO AI - Main Runner
=============================
Start the web server and run analysis.
"""

import os
import sys
import subprocess
import time
import signal

# Change to app directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def install_requirements():
    """Install required packages."""
    print("📦 Installing requirements...")
    result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Requirements installed!")
    else:
        print(f"❌ Error: {result.stderr}")
        sys.exit(1)

def run_analysis():
    """Run the betting analysis."""
    print("\n📊 Running betting analysis...")
    result = subprocess.run([sys.executable, 'app.py'], capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"Error: {result.stderr}")

def start_server():
    """Start the Flask web server."""
    print(f"\n🚀 Starting web server...")
    print(f"   Open: http://localhost:5000")
    print(f"   Press Ctrl+C to stop\n")
    
    # Start server
    os.execvp(sys.executable, [sys.executable, 'web_server.py'])

def main():
    """Main entry point."""
    print("\n" + "="*70)
    print("  ⚽ BETTING PRO AI - World's Best Tips App")
    print("="*70)
    
    # Check if requirements are installed
    try:
        import flask
        import requests
    except ImportError:
        install_requirements()
    
    # Run analysis first
    run_analysis()
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
