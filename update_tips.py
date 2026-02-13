#!/usr/bin/env python3
"""
Generate and push tips to deployed app
======================================
Run locally to update tips on Render.
"""

import requests
import json
from datetime import datetime

# Your deployed app URL
DEPLOYED_URL = "https://tippy-v8lb.onrender.com"
LOCAL_URL = "http://localhost:5000"

def trigger_analysis():
    """Trigger analysis on deployed app."""
    print("\n" + "="*70)
    print("🚀 GENERATING TIPS FOR DEPLOYED APP")
    print("="*70 + "\n")
    
    # Try deployed URL first
    urls = [DEPLOYED_URL, LOCAL_URL]
    
    for url in urls:
        print(f"🔗 Trying: {url}")
        
        try:
            # Trigger analysis
            print("📡 Running ML analysis...")
            response = requests.post(f"{url}/api/analyze", timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                tips = data.get('tips', [])
                stats = data.get('stats', {})
                
                print(f"\n✅ SUCCESS! Generated {len(tips)} tips\n")
                
                # Show top tips
                print("🎯 TOP TIPS:")
                print("-" * 70)
                
                for i, tip in enumerate(tips[:10], 1):
                    conf_emoji = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}[tip.get('confidence', 'LOW')]
                    
                    print(f"{conf_emoji} #{i} {tip['home_team']} vs {tip['away_team']}")
                    print(f"   📅 {tip['date']} | {tip['league']}")
                    print(f"   💡 Pick: {tip['prediction']} @ {tip['odds']:.2f}")
                    print(f"   📈 Edge: +{tip['edge']:.1f}% | Conf: {tip['confidence']}")
                    print(f"   💰 Kelly: {tip['kelly_pct']:.2f}% ({tip['kelly_units']} units)\n")
                
                # Show stats
                print("📊 STATS:")
                print(f"   Total Tips: {stats.get('total_tips', 0)}")
                print(f"   Pending: {stats.get('pending', 0)}")
                print(f"   Accuracy: {stats.get('accuracy', 0)}%")
                print(f"   ROI: {stats.get('roi_pct', 0):+.2f}%")
                
                print(f"\n🌐 View at: {url}")
                
                return True
                
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Connection failed: {e}")
    
    return False

def check_status():
    """Check app status."""
    urls = [DEPLOYED_URL, LOCAL_URL]
    
    for url in urls:
        try:
            print(f"\n🔍 Checking: {url}")
            response = requests.get(f"{url}/api/tips", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                tips = data.get('tips', [])
                stats = data.get('stats', {})
                
                print(f"\n✅ App is LIVE!")
                print(f"📊 Tips: {len(tips)}")
                print(f"📈 Stats: {stats}")
                
                return True
                
        except Exception as e:
            print(f"❌ {e}")
    
    return False

def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "status":
            check_status()
        else:
            print("Usage:")
            print("  python3 update_tips.py       # Generate tips")
            print("  python3 update_tips.py status  # Check status")
    else:
        success = trigger_analysis()
        
        if not success:
            print("\n" + "="*70)
            print("❌ Could not connect to deployed app.")
            print("\n📝 Possible reasons:")
            print("   1. App is still deploying (wait 2-5 min)")
            print("   2. API keys not configured")
            print("   3. App needs to be woken up")
            print("\n💡 Try visiting the URL in your browser first:")
            print(f"   {DEPLOYED_URL}")
            print("="*70)

if __name__ == "__main__":
    main()
