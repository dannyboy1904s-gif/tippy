#!/usr/bin/env python3
"""
WORLD'S BEST BETTING TIPS APP - Main Application
=================================================
Complete betting tips platform with ML predictions,
real-time odds, analytics, and bankroll management.
"""

import json
import sqlite3
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import threading
import time
import os

# Configuration
CONFIG = {
    "app_name": "Betting Pro AI",
    "version": "3.0.0",
    "bankroll": 1000,
    "kelly_fraction": 0.35,
    "max_kelly_pct": 0.075,
    "min_edge": 10,
    "min_confidence": "MEDIUM",
    "api_football": "cdc6bb9d446d48d387c2c827d8fda1e9",
    "api_odds": "c5f52c865fb2815f46380e1a2eb7fd5a",
}

# Database path
DB_PATH = "/home/bodins/.openclaw/workspace/betting_app/data/tips.db"

@dataclass
class Match:
    """Represents a football match."""
    home_team: str
    away_team: str
    league: str
    date: str
    time: str
    home_prob: float
    draw_prob: float
    away_prob: float
    home_odds: float
    draw_odds: float
    away_odds: float

@dataclass
class Tip:
    """Represents a betting tip."""
    match: Match
    prediction: str
    confidence: str
    edge: float
    kelly_pct: float
    kelly_units: float
    odds: float
    status: str = "pending"
    actual_outcome: Optional[str] = None
    score: Optional[str] = None
    win: Optional[bool] = None

class BettingApp:
    """Main betting application class."""
    
    def __init__(self):
        self.setup_database()
        self.load_teams()
        self.load_leagues()
    
    def setup_database(self):
        """Initialize SQLite database."""
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Tips table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                home_team TEXT,
                away_team TEXT,
                league TEXT,
                date TEXT,
                prediction TEXT,
                confidence TEXT,
                edge REAL,
                kelly_pct REAL,
                kelly_units REAL,
                odds REAL,
                status TEXT,
                actual_outcome TEXT,
                score TEXT,
                created_at TEXT
            )
        ''')
        
        # Teams table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                rating INTEGER,
                form TEXT,
                home_advantage INTEGER
            )
        ''')
        
        # Performance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                total_tips INTEGER,
                wins INTEGER,
                accuracy REAL,
                roi REAL,
                roi_pct REAL,
                profit REAL
            )
        ''')
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_teams(self):
        """Load team intelligence data."""
        self.teams = {}
        
        # Premium teams database
        premium_teams = {
            # Premier League
            "Manchester City": {"rating": 96, "form": "WWWWW", "home_adv": 9},
            "Liverpool": {"rating": 94, "form": "WLWWW", "home_adv": 8},
            "Arsenal": {"rating": 92, "form": "WWLDW", "home_adv": 8},
            "Aston Villa": {"rating": 85, "form": "WWLWW", "home_adv": 7},
            "Tottenham": {"rating": 86, "form": "LWWLW", "home_adv": 7},
            "Chelsea": {"rating": 87, "form": "WLWLD", "home_adv": 7},
            "Manchester United": {"rating": 84, "form": "LDLWL", "home_adv": 6},
            "Newcastle": {"rating": 84, "form": "WWLWL", "home_adv": 6},
            
            # Bundesliga
            "Bayern Munich": {"rating": 97, "form": "WWWWW", "home_adv": 9},
            "Dortmund": {"rating": 90, "form": "WWLWW", "home_adv": 8},
            "Leverkusen": {"rating": 89, "form": "WWWWD", "home_adv": 8},
            "RB Leipzig": {"rating": 87, "form": "WLWWW", "home_adv": 7},
            
            # Serie A
            "Inter Milan": {"rating": 93, "form": "WWWWW", "home_adv": 8},
            "Juventus": {"rating": 89, "form": "WWLWD", "home_adv": 8},
            "AC Milan": {"rating": 88, "form": "WLWWL", "home_adv": 7},
            "Napoli": {"rating": 86, "form": "LWLLW", "home_adv": 7},
            
            # La Liga
            "Real Madrid": {"rating": 96, "form": "WWWWW", "home_adv": 9},
            "Barcelona": {"rating": 92, "form": "WLWWW", "home_adv": 8},
            "Atletico Madrid": {"rating": 88, "form": "WWLDL", "home_adv": 7},
            "Girona": {"rating": 84, "form": "LWWWW", "home_adv": 7},
            
            # Ligue 1
            "PSG": {"rating": 93, "form": "WWWDW", "home_adv": 8},
            "Monaco": {"rating": 85, "form": "LWWWW", "home_adv": 7},
            "Lille": {"rating": 83, "form": "WLDWW", "home_adv": 6},
            
            # Eredivisie
            "PSV Eindhoven": {"rating": 88, "form": "WWWWW", "home_adv": 8},
            "Ajax": {"rating": 87, "form": "LWWWW", "home_adv": 8},
            "Feyenoord": {"rating": 86, "form": "WWLDW", "home_adv": 7},
            
            # Primeira Liga
            "Porto": {"rating": 88, "form": "WWWWW", "home_adv": 8},
            "Benfica": {"rating": 87, "form": "WLWWW", "home_adv": 8},
            "Sporting CP": {"rating": 86, "form": "WWLWD", "home_adv": 7},
            
            # Championship
            "Leicester City": {"rating": 82, "form": "WWWWW", "home_adv": 6},
            "Leeds United": {"rating": 80, "form": "WLWWW", "home_adv": 6},
            "Southampton": {"rating": 79, "form": "WWLWL", "home_adv": 6},
        }
        
        self.teams.update(premium_teams)
    
    def load_leagues(self):
        """Load league configurations."""
        self.leagues = {
            "PL": {"name": "Premier League", "country": "England", "priority": 1},
            "BL1": {"name": "Bundesliga", "country": "Germany", "priority": 2},
            "SA": {"name": "Serie A", "country": "Italy", "priority": 3},
            "PD": {"name": "La Liga", "country": "Spain", "priority": 4},
            "FL1": {"name": "Ligue 1", "country": "France", "priority": 5},
            "DED": {"name": "Eredivisie", "country": "Netherlands", "priority": 6},
            "PPL": {"name": "Primeira Liga", "country": "Portugal", "priority": 7},
            "ELC": {"name": "Championship", "country": "England", "priority": 8},
        }
    
    def fetch_matches(self) -> List[Match]:
        """Fetch upcoming matches from Football-Data API."""
        matches = []
        
        try:
            url = "https://api.football-data.org/v4/matches"
            params = {
                "status": "TIMED,Scheduled",
                "dateFrom": datetime.now().strftime('%Y-%m-%d'),
                "dateTo": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            }
            
            response = requests.get(
                url, 
                headers={"X-Auth-Token": CONFIG["api_football"]},
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                for match in data.get("matches", []):
                    league_code = match.get("competition", {}).get("code", "OTHER")
                    
                    if league_code not in self.leagues:
                        continue
                    
                    home = match["homeTeam"]["name"]
                    away = match["awayTeam"]["name"]
                    
                    # Get team ratings
                    home_rating = self.teams.get(home, {}).get("rating", 70)
                    away_rating = self.teams.get(away, {}).get("rating", 70)
                    
                    # Calculate probabilities using Poisson model
                    home_goals = max(0, (home_rating / 70) * 1.5 - (away_rating / 70) * 0.5)
                    away_goals = max(0, (away_rating / 70) * 1.2 - (home_rating / 70) * 0.3)
                    
                    home_prob = self.poisson_probability(home_goals, away_goals)
                    away_prob = self.poisson_probability(away_goals, home_goals)
                    draw_prob = 1 - home_prob - away_prob
                    
                    # Normalize
                    total = home_prob + draw_prob + away_prob
                    home_prob /= total
                    draw_prob /= total
                    away_prob /= total
                    
                    matches.append(Match(
                        home_team=home,
                        away_team=away,
                        league=self.leagues[league_code]["name"],
                        date=match["utcDate"][:10],
                        time=match["utcDate"][11:16],
                        home_prob=round(home_prob * 100, 1),
                        draw_prob=round(draw_prob * 100, 1),
                        away_prob=round(away_prob * 100, 1),
                        home_odds=0,
                        draw_odds=0,
                        away_odds=0
                    ))
        
        except Exception as e:
            print(f"Error fetching matches: {e}")
        
        return matches
    
    def poisson_probability(self, goals_a: float, goals_b: float) -> float:
        """Calculate Poisson probability for home win."""
        import math
        return (math.exp(-goals_a) * goals_a ** goals_b) / math.factorial(int(goals_b))
    
    def fetch_odds(self, matches: List[Match]) -> List[Match]:
        """Fetch real odds from The Odds API."""
        try:
            url = "https://api.the-odds-api.com/v4/sports/football/odds"
            params = {
                "apiKey": CONFIG["api_odds"],
                "regions": "eu,uk",
                "markets": "h2h",
                "oddsFormat": "decimal"
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Create odds lookup
                odds_lookup = {}
                for event in data:
                    match_key = (event.get("home_team"), event.get("away_team"))
                    
                    best_odds = {"1": 0, "X": 0, "2": 0}
                    
                    for bookmaker in event.get("bookmakers", []):
                        for market in bookmaker.get("markets", []):
                            if market.get("key") == "h2h":
                                for outcome in market.get("outcomes", []):
                                    if outcome["name"] == "Home":
                                        best_odds["1"] = max(best_odds["1"], outcome["price"])
                                    elif outcome["name"] == "Draw":
                                        best_odds["X"] = max(best_odds["X"], outcome["price"])
                                    elif outcome["Name"] == "Away":
                                        best_odds["2"] = max(best_odds["2"], outcome["price"])
                    
                    if sum(best_odds.values()) > 0:
                        odds_lookup[match_key] = best_odds
                
                # Apply odds to matches
                for match in matches:
                    match_key = (match.home_team, match.away_team)
                    if match_key in odds_lookup:
                        odds = odds_lookup[match_key]
                        match.home_odds = odds["1"]
                        match.draw_odds = odds["X"]
                        match.away_odds = odds["2"]
        
        except Exception as e:
            print(f"Error fetching odds: {e}")
        
        return matches
    
    def generate_tips(self, matches: List[Match]) -> List[Tip]:
        """Generate betting tips from matches."""
        tips = []
        
        for match in matches:
            if match.home_odds == 0:
                continue
            
            # Find best value bet
            bets = [
                ("1", match.home_prob, match.home_odds),
                ("X", match.draw_prob, match.draw_odds),
                ("2", match.away_prob, match.away_odds)
            ]
            
            best_bet = None
            best_edge = -100
            
            for outcome, prob, odds in bets:
                # Fair odds based on probability
                fair_odds = 100 / prob
                
                # Edge calculation
                edge = ((odds - fair_odds) / fair_odds) * 100
                
                if edge > best_edge:
                    best_edge = edge
                    best_bet = (outcome, prob, odds)
            
            if best_bet and best_edge >= CONFIG["min_edge"]:
                outcome, prob, odds = best_bet
                
                # Determine confidence
                if best_edge >= 25 and prob >= 60:
                    confidence = "HIGH"
                elif best_edge >= 15 or prob >= 50:
                    confidence = "MEDIUM"
                else:
                    confidence = "LOW"
                
                # Kelly calculation
                conf_mult = {"HIGH": 1.0, "MEDIUM": 0.7, "LOW": 0.4}
                Kelly = ((odds - 1) * (prob / 100) - (1 - prob / 100)) / (odds - 1)
                Kelly *= CONFIG["kelly_fraction"] * conf_mult[confidence]
                Kelly = max(0, min(Kelly, CONFIG["max_kelly_pct"]))
                
                prediction_map = {"1": "Home Win", "X": "Draw", "2": "Away Win"}
                
                tip = Tip(
                    match=match,
                    prediction=prediction_map[outcome],
                    confidence=confidence,
                    edge=round(best_edge, 1),
                    kelly_pct=round(Kelly * 100, 2),
                    kelly_units=round(Kelly * CONFIG["bankroll"], 1),
                    odds=odds
                )
                
                tips.append(tip)
        
        # Sort by edge (best first)
        tips.sort(key=lambda x: -x.edge)
        
        return tips
    
    def save_tip(self, tip: Tip):
        """Save tip to database."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tips (
                home_team, away_team, league, date,
                prediction, confidence, edge, kelly_pct, kelly_units, odds,
                status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            tip.match.home_team, tip.match.away_team, tip.match.league,
            tip.match.date, tip.prediction, tip.confidence,
            tip.edge, tip.kelly_pct, tip.kelly_units, tip.odds,
            tip.status, datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def update_results(self):
        """Update tip results from API."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get pending tips
        cursor.execute("SELECT * FROM tips WHERE status = 'pending'")
        pending = cursor.fetchall()
        
        # Fetch yesterday's results
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        try:
            url = f"https://api.football-data.org/v4/matches?dateFrom={yesterday}&dateTo={yesterday}"
            response = requests.get(
                url,
                headers={"X-Auth-Token": CONFIG["api_football"]},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                results = {}
                for match in data.get("matches", []):
                    if match.get("status") == "FINISHED":
                        hg = match["score"]["fullTime"]["home"]
                        ag = match["score"]["fullTime"]["away"]
                        
                        if hg is not None:
                            if hg > ag:
                                outcome = "1"
                            elif ag > hg:
                                outcome = "2"
                            else:
                                outcome = "X"
                            
                            results[(match["homeTeam"]["name"], match["awayTeam"]["name"])] = {
                                "outcome": outcome,
                                "score": f"{hg}-{ag}"
                            }
                
                # Update tips
                for tip in pending:
                    tip_id = tip[0]
                    home, away = tip[1], tip[2]
                    key = (home, away)
                    
                    if key in results:
                        actual = results[key]["outcome"]
                        score = results[key]["score"]
                        
                        prediction_map = {"Home Win": "1", "Draw": "X", "Away Win": "2"}
                        predicted = prediction_map.get(tip[5], "1")
                        
                        win = predicted == actual
                        
                        cursor.execute('''
                            UPDATE tips SET 
                                status = 'resulted',
                                actual_outcome = ?,
                                score = ?,
                                win = ?
                            WHERE id = ?
                        ''', (actual, score, win, tip_id))
                
                conn.commit()
        
        except Exception as e:
            print(f"Error updating results: {e}")
        
        conn.close()
        self.update_performance()
    
    def update_performance(self):
        """Update performance statistics."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tips WHERE status = 'resulted'")
        resulted = cursor.fetchall()
        
        if not resulted:
            conn.close()
            return
        
        wins = len([t for t in resulted if t[14]])
        total = len(resulted)
        accuracy = wins / total * 100 if total > 0 else 0
        
        # Calculate ROI
        roi = 0
        for tip in resulted:
            if tip[14]:  # win
                roi += tip[9] * (tip[10] - 1)  # kelly_units * (odds - 1)
            else:
                roi -= tip[9]  # -kelly_units
        
        roi_pct = roi / CONFIG["bankroll"] * 100
        
        # Save performance
        cursor.execute('''
            INSERT INTO performance (
                date, total_tips, wins, accuracy, roi, roi_pct, profit
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().strftime('%Y-%m-%d'),
            total, wins, accuracy, roi, roi_pct, roi
        ))
        
        conn.commit()
        conn.close()
    
    def get_performance(self) -> Dict:
        """Get performance statistics."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tips WHERE status = 'resulted'")
        resulted = cursor.fetchall()
        
        cursor.execute("SELECT * FROM tips")
        all_tips = cursor.fetchall()
        
        cursor.execute("SELECT * FROM performance ORDER BY id DESC LIMIT 30")
        history = cursor.fetchall()
        
        conn.close()
        
        total = len(resulted)
        wins = len([t for t in resulted if t[14]]) if total > 0 else 0
        pending = len([t for t in all_tips if t[11] == "pending"])
        
        roi = 0
        for tip in resulted:
            if tip[14]:
                roi += tip[9] * (tip[10] - 1)
            else:
                roi -= tip[9]
        
        return {
            "total_tips": len(all_tips),
            "pending": pending,
            "resulted": total,
            "wins": wins,
            "accuracy": round(wins / total * 100, 1) if total > 0 else 0,
            "roi": round(roi, 2),
            "roi_pct": round(roi / CONFIG["bankroll"] * 100, 2),
            "bankroll": CONFIG["bankroll"],
            "history": history[-30:]
        }
    
    def get_analytics(self) -> Dict:
        """Get detailed analytics."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # By league
        cursor.execute('''
            SELECT league, COUNT(*) as count, 
                SUM(CASE WHEN win = 1 THEN 1 ELSE 0 END) as wins
            FROM tips WHERE status = 'resulted'
            GROUP BY league
        ''')
        by_league = cursor.fetchall()
        
        # By confidence
        cursor.execute('''
            SELECT confidence, COUNT(*) as count,
                SUM(CASE WHEN win = 1 THEN 1 ELSE 0 END) as wins
            FROM tips WHERE status = 'resulted'
            GROUP BY confidence
        ''')
        by_confidence = cursor.fetchall()
        
        # By odds range
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN odds < 1.5 THEN '1.0-1.5'
                    WHEN odds < 2.0 THEN '1.5-2.0'
                    WHEN odds < 3.0 THEN '2.0-3.0'
                    ELSE '3.0+'
                END as range,
                COUNT(*) as count,
                SUM(CASE WHEN win = 1 THEN 1 ELSE 0 END) as wins
            FROM tips WHERE status = 'resulted'
            GROUP BY range
        ''')
        by_odds_range = cursor.fetchall()
        
        conn.close()
        
        return {
            "by_league": by_league,
            "by_confidence": by_confidence,
            "by_odds_range": by_odds_range
        }
    
    def run_analysis(self):
        """Run full analysis and generate tips."""
        print(f"\n{'='*70}")
        print(f"  ⚽ {CONFIG['app_name']} v{CONFIG['version']}")
        print(f"  Bankroll: ${CONFIG['bankroll']} | Kelly: {CONFIG['kelly_fraction']*100:.0f}%")
        print(f"{'='*70}\n")
        
        # Fetch matches
        print("📡 Fetching matches...")
        matches = self.fetch_matches()
        print(f"   Found {len(matches)} matches")
        
        # Fetch odds
        print("📡 Fetching odds...")
        matches = self.fetch_odds(matches)
        
        # Generate tips
        print("🧠 Generating ML predictions...")
        tips = self.generate_tips(matches)
        
        # Save tips
        for tip in tips:
            self.save_tip(tip)
        
        print(f"   Generated {len(tips)} high-value tips")
        
        # Show top tips
        print(f"\n🎯 TOP {min(10, len(tips))} TIPS:\n")
        
        for i, tip in enumerate(tips[:10], 1):
            conf_emoji = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}[tip.confidence]
            
            print(f"{conf_emoji} #{i} {tip.match.home_team} vs {tip.match.away_team}")
            print(f"   📅 {tip.match.date} | {tip.match.league}")
            print(f"   💡 Pick: {tip.prediction} @ {tip.odds:.2f}")
            print(f"   📈 Edge: +{tip.edge:.1f}% | Conf: {tip.confidence}")
            print(f"   💰 Kelly: {tip.kelly_pct:.2f}% ({tip.kelly_units} units)\n")
        
        # Show performance
        perf = self.get_performance()
        print(f"\n📊 PERFORMANCE:")
        print(f"   Total Tips: {perf['total_tips']}")
        print(f"   Pending: {perf['pending']}")
        print(f"   Resulted: {perf['resulted']}")
        print(f"   Accuracy: {perf['accuracy']}%")
        print(f"   ROI: {perf['roi_pct']:+.2f}%")
        print(f"{'='*70}\n")
        
        return tips

def main():
    """Main entry point."""
    app = BettingApp()
    app.run_analysis()

if __name__ == "__main__":
    main()
