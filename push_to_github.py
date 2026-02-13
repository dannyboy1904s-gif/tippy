#!/usr/bin/env python3
"""
GitHub Push Script for Betting Pro AI
======================================
Push to GitHub with one command.
"""

import os
import subprocess

def run_command(cmd):
    """Run shell command."""
    print(f"⚙️  {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0 and result.stderr:
        print(f"❌ {result.stderr}")
        return False
    return True

def main():
    print("\n" + "="*70)
    print("🚀 PUSHING TO GITHUB")
    print("="*70 + "\n")
    
    # Get GitHub username
    username = input("👤 Enter your GitHub username: ").strip()
    
    if not username:
        print("❌ Username is required!")
        return
    
    repo_name = "betting-pro-ai"
    repo_url = f"https://github.com/{username}/{repo_name}.git"
    
    print(f"\n📦 Repository: {repo_url}\n")
    
    # Initialize git if not exists
    if not os.path.exists('.git'):
        print("📦 Initializing git...")
        run_command("git init")
        run_command("git add .")
        run_command('git commit -m "Initial commit: Betting Pro AI v3.0 - ML-powered betting predictions"')
    else:
        print("✅ Git already initialized")
        run_command("git add .")
        run_command('git commit -m "Update: Betting Pro AI v3.0"')
    
    # Check if remote exists
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    
    if "origin" in result.stdout:
        print("\n🔗 Remote 'origin' already exists")
        print(f"   URL: {result.stdout.split()[1]}")
    else:
        print(f"\n🔗 Adding remote origin...")
        run_command(f"git remote add origin {repo_url}")
    
    # Push
    print(f"\n🚀 Pushing to GitHub...")
    success = run_command("git branch -M main")
    
    if success:
        push_result = subprocess.run("git push -u origin main", shell=True, capture_output=True, text=True)
        
        if push_result.returncode == 0:
            print("\n" + "="*70)
            print("✅ SUCCESS! Code pushed to GitHub!")
            print("="*70)
            print(f"\n🌐 Your repository:")
            print(f"   https://github.com/{username}/{repo_name}")
            print(f"\n🎯 NEXT STEPS:")
            print("-" * 70)
            print("""
1. Go to: https://dashboard.render.com
2. Sign up/login with GitHub
3. Click "New +" → "Web Service"
4. Select repository: betting-pro-ai
5. Configure:
   - Name: betting-pro-ai
   - Build: pip install -r requirements.txt
   - Start: gunicorn web_server:app
   - Plan: Free
6. Click "Create Web Service"

✅ Your app will be live at:
   https://betting-pro-ai.onrender.com
""")
            print("="*70)
        else:
            print("\n❌ Push failed. Possible reasons:")
            print("   - Repository doesn't exist yet")
            print("   - Authentication required")
            print("\n📝 Create repository first:")
            print(f"   → Go to: https://github.com/new")
            print(f"   → Name: {repo_name}")
            print(f"   → Public or Private")
            print(f"   → Click 'Create'")
            print(f"\n🔄 Then try pushing again:")
            print(f"   git push -u origin main")

if __name__ == "__main__":
    main()
