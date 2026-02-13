#!/usr/bin/env python3
"""Simple test script for deployed app."""

import requests
import time

URL = "https://tippy-v8lb.onrender.com"

print(f"\n🔍 Testing: {URL}\n")

# Try multiple times
for i in range(3):
    print(f"Attempt {i+1}/3...")
    
    # Try root
    try:
        r = requests.get(URL, timeout=15)
        print(f"  Root: {r.status_code}")
    except Exception as e:
        print(f"  Root error: {e}")
    
    # Try API
    try:
        r = requests.get(f"{URL}/api/tips", timeout=15)
        print(f"  /api/tips: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"  Tips: {len(data.get('tips', []))}")
            break
    except Exception as e:
        print(f"  API error: {e}")
    
    time.sleep(3)

print("\n📊 If all fail, check Render dashboard for build logs.")
