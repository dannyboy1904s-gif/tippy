#!/usr/bin/env python3
"""
Deploy Script for Betting Pro AI
================================
Deploy to Render.com with one click.
"""

import os
import subprocess
import sys

def run_command(cmd, capture=True):
    """Run a shell command."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    if capture:
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(f"Error: {result.stderr}")
            return False
    return True

def check_git():
    """Check if git is initialized."""
    if not os.path.exists('.git'):
        print("📦 Initializing git repository...")
        run_command("git init")
        run_command("git add .")
        run_command('git commit -m "Initial commit: Betting Pro AI v3.0"')
    else:
        print("✅ Git already initialized")

def check_files():
    """Check if required files exist."""
    required = ['app.py', 'web_server.py', 'requirements.txt', 'Procfile']
    missing = []
    
    for f in required:
        if not os.path.exists(f):
            missing.append(f)
    
    if missing:
        print(f"❌ Missing files: {', '.join(missing)}")
        return False
    
    print("✅ All required files present")
    return True

def prepare_deployment():
    """Prepare files for deployment."""
    print("\n" + "="*60)
    print("🚀 DEPLOYING BETTING PRO AI")
    print("="*60)
    
    # Check files
    if not check_files():
        sys.exit(1)
    
    # Check git
    check_git()
    
    # Create GitHub repo
    print("\n📋 NEXT STEPS:")
    print("-" * 60)
    print("""
1. Create a repository on GitHub:
   → Go to: https://github.com/new
   → Name: betting-pro-ai
   → Public or Private
   → Click 'Create repository'

2. Push your code:
""")
    
    # Get current directory name
    cwd = os.path.basename(os.path.abspath('.'))
    print(f"   cd {cwd}")
    print(f"   git remote add origin https://github.com/YOUR_USERNAME/betting-pro-ai.git")
    print(f"   git push -u origin main")
    
    print("""
3. Deploy on Render.com:
   → Go to: https://dashboard.render.com
   → Sign up with GitHub
   → Click 'New +' → 'Web Service'
   → Select your repository
   → Configure:
     - Name: betting-pro-ai
     - Build: pip install -r requirements.txt
     - Start: gunicorn web_server:app
     - Plan: Free
   → Click 'Create Web Service'

4. Your app will be live at:
   → https://betting-pro-ai.onrender.com

""")
    
    print("="*60)
    print("✅ Ready to deploy!")
    print("="*60)

if __name__ == "__main__":
    prepare_deployment()
