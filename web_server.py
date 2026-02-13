#!/usr/bin/env python3
"""
Betting Pro AI - Flask Web Server
==================================
API server for the betting tips web app.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import BettingApp, CONFIG

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')
CORS(app)

# Initialize app
betting_app = BettingApp()

# Serve static files
@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# API Routes
@app.route('/api/tips')
def get_tips():
    """Get all current tips."""
    try:
        # Load tips from database
        import sqlite3
        conn = sqlite3.connect(betting_app.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tips WHERE status = 'pending' ORDER BY edge DESC")
        tips = cursor.fetchall()
        conn.close()
        
        tips_data = []
        for tip in tips:
            tips_data.append({
                'id': tip[0],
                'home_team': tip[1],
                'away_team': tip[2],
                'league': tip[3],
                'date': tip[4],
                'prediction': tip[5],
                'confidence': tip[6],
                'edge': tip[7],
                'kelly_pct': tip[8],
                'kelly_units': tip[9],
                'odds': tip[10],
                'status': tip[11]
            })
        
        # Get stats
        stats = betting_app.get_performance()
        
        return jsonify({
            'tips': tips_data,
            'stats': {
                'total_tips': stats['total_tips'],
                'pending': stats['pending'],
                'resulted': stats['resulted'],
                'wins': stats['wins'],
                'accuracy': stats['accuracy'],
                'roi': stats['roi'],
                'roi_pct': stats['roi_pct'],
                'profit': round(stats['roi'], 2)
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def run_analysis():
    """Run full analysis and generate tips."""
    try:
        tips = betting_app.run_analysis()
        
        tips_data = []
        for tip in tips:
            tips_data.append({
                'home_team': tip.match.home_team,
                'away_team': tip.match.away_team,
                'league': tip.match.league,
                'date': tip.match.date,
                'time': tip.match.time,
                'prediction': tip.prediction,
                'confidence': tip.confidence,
                'edge': tip.edge,
                'kelly_pct': tip.kelly_pct,
                'kelly_units': tip.kelly_units,
                'odds': tip.odds
            })
        
        stats = betting_app.get_performance()
        
        return jsonify({
            'tips': tips_data,
            'stats': {
                'total_tips': stats['total_tips'],
                'pending': stats['pending'],
                'resulted': stats['resulted'],
                'wins': stats['wins'],
                'accuracy': stats['accuracy'],
                'roi': stats['roi'],
                'roi_pct': stats['roi_pct'],
                'profit': round(stats['roi'], 2)
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance')
def get_performance():
    """Get performance statistics."""
    try:
        perf = betting_app.get_performance()
        analytics = betting_app.get_analytics()
        
        return jsonify({
            'performance': perf,
            'analytics': analytics
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history')
def get_history():
    """Get betting history."""
    try:
        import sqlite3
        conn = sqlite3.connect(betting_app.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tips WHERE status = 'resulted' ORDER BY date DESC LIMIT 50")
        history = cursor.fetchall()
        conn.close()
        
        history_data = []
        for bet in history:
            history_data.append({
                'date': bet[4],
                'home_team': bet[1],
                'away_team': bet[2],
                'prediction': bet[5],
                'odds': bet[10],
                'actual_outcome': bet[12],
                'score': bet[13],
                'win': bet[14],
                'profit': round(bet[9] * (bet[10] - 1), 2) if bet[14] else round(-bet[9], 2)
            })
        
        return jsonify({'history': history_data})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    """Get or update settings."""
    try:
        if request.method == 'POST':
            new_settings = request.json
            
            # Update config
            if 'bankroll' in new_settings:
                CONFIG['bankroll'] = new_settings['bankroll']
            if 'kelly_fraction' in new_settings:
                CONFIG['kelly_fraction'] = new_settings['kelly_fraction']
            if 'max_kelly_pct' in new_settings:
                CONFIG['max_kelly_pct'] = new_settings['max_kelly_pct']
            if 'min_edge' in new_settings:
                CONFIG['min_edge'] = new_settings['min_edge']
            
            # Save to database
            import sqlite3
            conn = sqlite3.connect(betting_app.DB_PATH)
            cursor = conn.cursor()
            
            for key, value in new_settings.items():
                cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", 
                              (key, json.dumps(value)))
            
            conn.commit()
            conn.close()
            
            return jsonify({'success': True})
        
        else:
            # Get settings
            return jsonify({
                'bankroll': CONFIG['bankroll'],
                'kelly_fraction': CONFIG['kelly_fraction'],
                'max_kelly_pct': CONFIG['max_kelly_pct'],
                'min_edge': CONFIG['min_edge']
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/leagues')
def get_leagues():
    """Get available leagues."""
    return jsonify({'leagues': betting_app.leagues})

@app.route('/api/teams')
def get_teams():
    """Get team intelligence."""
    return jsonify({'teams': betting_app.teams})

@app.route('/api/update-results', methods=['POST'])
def update_results():
    """Update tip results."""
    try:
        betting_app.update_results()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"\n{'='*70}")
    print(f"  ⚽ Betting Pro AI - Web Server")
    print(f"  Version: {CONFIG['version']}")
    print(f"{'='*70}\n")
    
    # Run analysis on startup
    print("Running initial analysis...")
    betting_app.run_analysis()
    
    # Start server
    print(f"\n🚀 Server running at: http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
