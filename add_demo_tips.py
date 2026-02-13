#!/usr/bin/env python3
"""
Generate Demo Tips for Betting Pro AI
======================================
Add sample tips for demonstration when API limits are reached.
"""

import sqlite3
import json
from datetime import datetime, timedelta

DB_PATH = "/home/bodins/.openclaw/workspace/betting_app/data/tips.db"

# Demo tips (for demonstration)
DEMO_TIPS = [
    {
        "home_team": "Manchester City",
        "away_team": "Liverpool",
        "league": "Premier League",
        "date": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        "prediction": "Home Win",
        "confidence": "HIGH",
        "edge": 28.5,
        "kelly_pct": 4.2,
        "kelly_units": 42,
        "odds": 2.15
    },
    {
        "home_team": "Bayern Munich",
        "away_team": "Dortmund",
        "league": "Bundesliga",
        "date": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
        "prediction": "Home Win",
        "confidence": "HIGH",
        "edge": 24.3,
        "kelly_pct": 5.1,
        "kelly_units": 51,
        "odds": 1.95
    },
    {
        "home_team": "Real Madrid",
        "away_team": "Barcelona",
        "league": "La Liga",
        "date": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        "prediction": "Draw",
        "confidence": "MEDIUM",
        "edge": 18.7,
        "kelly_pct": 3.2,
        "kelly_units": 32,
        "odds": 3.40
    },
    {
        "home_team": "Inter Milan",
        "away_team": "Juventus",
        "league": "Serie A",
        "date": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
        "prediction": "Home Win",
        "confidence": "MEDIUM",
        "edge": 15.2,
        "kelly_pct": 2.8,
        "kelly_units": 28,
        "odds": 2.45
    },
    {
        "home_team": "PSG",
        "away_team": "Monaco",
        "league": "Ligue 1",
        "date": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        "prediction": "Home Win",
        "confidence": "MEDIUM",
        "edge": 12.5,
        "kelly_pct": 2.1,
        "kelly_units": 21,
        "odds": 1.75
    },
    {
        "home_team": "PSV Eindhoven",
        "away_team": "Ajax",
        "league": "Eredivisie",
        "date": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
        "prediction": "Away Win",
        "confidence": "MEDIUM",
        "edge": 11.8,
        "kelly_pct": 1.9,
        "kelly_units": 19,
        "odds": 2.85
    },
    {
        "home_team": "Porto",
        "away_team": "Benfica",
        "league": "Primeira Liga",
        "date": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
        "prediction": "Home Win",
        "confidence": "LOW",
        "edge": 10.2,
        "kelly_pct": 1.5,
        "kelly_units": 15,
        "odds": 2.20
    },
    {
        "home_team": "Arsenal",
        "away_team": "Tottenham",
        "league": "Premier League",
        "date": (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d'),
        "prediction": "Home Win",
        "confidence": "HIGH",
        "edge": 22.1,
        "kelly_pct": 4.8,
        "kelly_units": 48,
        "odds": 1.88
    },
    {
        "home_team": "Leverkusen",
        "away_team": "RB Leipzig",
        "league": "Bundesliga",
        "date": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
        "prediction": "Home Win",
        "confidence": "MEDIUM",
        "edge": 14.5,
        "kelly_pct": 2.5,
        "kelly_units": 25,
        "odds": 2.10
    },
    {
        "home_team": "AC Milan",
        "away_team": "Napoli",
        "league": "Serie A",
        "date": (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d'),
        "prediction": "Draw",
        "confidence": "LOW",
        "edge": 10.5,
        "kelly_pct": 1.6,
        "kelly_units": 16,
        "odds": 3.25
    }
]

def add_demo_tips():
    """Add demo tips to database."""
    print("\n" + "="*70)
    print("🎯 ADDING DEMO TIPS")
    print("="*70 + "\n")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Clear existing pending tips
    cursor.execute("DELETE FROM tips WHERE status = 'pending'")
    print("🗑️ Cleared pending tips")
    
    # Add demo tips
    for tip in DEMO_TIPS:
        cursor.execute('''
            INSERT INTO tips (
                home_team, away_team, league, date,
                prediction, confidence, edge, kelly_pct, kelly_units, odds,
                status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            tip["home_team"],
            tip["away_team"],
            tip["league"],
            tip["date"],
            tip["prediction"],
            tip["confidence"],
            tip["edge"],
            tip["kelly_pct"],
            tip["kelly_units"],
            tip["odds"],
            "pending",
            datetime.now().isoformat()
        ))
        
        print(f"✅ Added: {tip['home_team']} vs {tip['away_team']}")
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Added {len(DEMO_TIPS)} demo tips!")
    print("="*70 + "\n")

def add_sample_performance():
    """Add sample performance history."""
    print("\n📊 Adding sample performance data...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Sample historical performance
    sample_data = [
        {"date": "2026-02-10", "total_tips": 5, "wins": 3, "accuracy": 60, "roi": 8.5, "roi_pct": 0.85, "profit": 85},
        {"date": "2026-02-11", "total_tips": 7, "wins": 5, "accuracy": 71.4, "roi": 12.2, "roi_pct": 1.22, "profit": 122},
        {"date": "2026-02-12", "total_tips": 4, "wins": 2, "accuracy": 50, "roi": -2.5, "roi_pct": -0.25, "profit": -25},
        {"date": "2026-02-13", "total_tips": 6, "wins": 4, "accuracy": 66.7, "roi": 9.8, "roi_pct": 0.98, "profit": 98},
    ]
    
    for data in sample_data:
        cursor.execute('''
            INSERT INTO performance (date, total_tips, wins, accuracy, roi, roi_pct, profit)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data["date"], data["total_tips"], data["wins"], data["accuracy"],
            data["roi"], data["roi_pct"], data["profit"]
        ))
    
    conn.commit()
    conn.close()
    
    print("✅ Added performance history!")

if __name__ == "__main__":
    add_demo_tips()
    add_sample_performance()
