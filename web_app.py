#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NHL Injury Feed Web Application
Serves injury data on a webpage with compact team grid layout
"""

from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime
from threading import Thread
import time
import schedule
from simple_injury_scraper import scrape_hockey_reference_injuries, format_injury_report

app = Flask(__name__)

# Global data storage
injury_data = {
    'injuries': [],
    'last_updated': None,
    'total_count': 0,
    'by_team': {},
    'team_grid': []
}

# NHL Team Information with logos and divisions
NHL_TEAMS = {
    'ANA': {'name': 'Anaheim Ducks', 'logo': '🦆', 'division': 'Pacific'},
    'BOS': {'name': 'Boston Bruins', 'logo': '🐻', 'division': 'Atlantic'},
    'BUF': {'name': 'Buffalo Sabres', 'logo': ⚔️', 'division': 'Atlantic'},
    'CGY': {'name': 'Calgary Flames', 'logo': '🔥', 'division': 'Pacific'},
    'CAR': {'name': 'Carolina Hurricanes', 'logo': '🌀', 'division': 'Metropolitan'},
    'CHI': {'name': 'Chicago Blackhawks', 'logo': '🪶', 'division': 'Central'},
    'COL': {'name': 'Colorado Avalanche', 'logo': '🏔️', 'division': 'Central'},
    'CBJ': {'name': 'Columbus Blue Jackets', 'logo': '🧥', 'division': 'Metropolitan'},
    'DAL': {'name': 'Dallas Stars', 'logo': '⭐', 'division': 'Central'},
    'DET': {'name': 'Detroit Red Wings', 'logo': '🪽', 'division': 'Atlantic'},
    'EDM': {'name': 'Edmonton Oilers', 'logo': '🛢️', 'division': 'Pacific'},
    'FLA': {'name': 'Florida Panthers', 'logo': '🐾', 'division': 'Atlantic'},
    'LAK': {'name': 'Los Angeles Kings', 'logo': '👑', 'division': 'Pacific'},
    'MIN': {'name': 'Minnesota Wild', 'logo': '🌲', 'division': 'Central'},
    'MTL': {'name': 'Montreal Canadiens', 'logo': '🇨🇦', 'division': 'Atlantic'},
    'NSH': {'name': 'Nashville Predators', 'logo': '🎸', 'division': 'Central'},
    'NJD': {'name': 'New Jersey Devils', 'logo': '😈', 'division': 'Metropolitan'},
    'NYI': {'name': 'New York Islanders', 'logo': '🏝️', 'division': 'Metropolitan'},
    'NYR': {'name': 'New York Rangers', 'logo': '🗽', 'division': 'Metropolitan'},
    'OTT': {'name': 'Ottawa Senators', 'logo': '🏛️', 'division': 'Atlantic'},
    'PHI': {'name': 'Philadelphia Flyers', 'logo': '🧡', 'division': 'Metropolitan'},
    'PIT': {'name': 'Pittsburgh Penguins', 'logo': '🐧', 'division': 'Metropolitan'},
    'SJS': {'name': 'San Jose Sharks', 'logo': '🦈', 'division': 'Pacific'},
    'SEA': {'name': 'Seattle Kraken', 'logo': '🐙', 'division': 'Pacific'},
    'STL': {'name': 'St. Louis Blues', 'logo': '🎵', 'division': 'Central'},
    'TBL': {'name': 'Tampa Bay Lightning', 'logo': '⚡', 'division': 'Atlantic'},
    'TOR': {'name': 'Toronto Maple Leafs', 'logo': '🍁', 'division': 'Atlantic'},
    'UTA': {'name': 'Utah Hockey Club', 'logo': '🏔️', 'division': 'Central'},
    'VAN': {'name': 'Vancouver Canucks', 'logo': '🌊', 'division': 'Pacific'},
    'VGK': {'name': 'Vegas Golden Knights', 'logo': '⚜️', 'division': 'Pacific'},
    'WSH': {'name': 'Washington Capitals', 'logo': '🏛️', 'division': 'Metropolitan'},
    'WPG': {'name': 'Winnipeg Jets', 'logo': '✈️', 'division': 'Central'}
}

def sort_injuries_by_date(injuries):
    """Sort injuries in reverse chronological order (newest first)."""
    def get_sort_key(injury):
        injury_date = injury.get('injury_date', '')
        scraped_at = injury.get('scraped_at', '')
        # Try to parse injury_date first, then scraped_at, then current time
        for date_str in [injury_date, scraped_at]:
            if date_str:
                try:
                    if 'T' in date_str:  # ISO format
                        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    else:  # Simple date format
                        return datetime.strptime(date_str, '%Y-%m-%d')
                except (ValueError, TypeError):
                    continue
        return datetime.now()
    return sorted(injuries, key=get_sort_key, reverse=True)

def create_team_grid_with_injuries():
    """Create compact team grid with all teams visible on one screen."""
    grid_data = {}
    # Initialize all teams
    for team_code, team_info in NHL_TEAMS.items():
        grid_data[team_code] = {'name': team_info['name'], 'logo': team_info['logo'], 'division': team_info['division'], 'injuries': [], 'injury_count': 0}
    # Add injury data to respective teams
    for injury in injury_data['injuries']:
        team_code = injury.get('team')
        if team_code in grid_data:
            grid_data[team_code]['injuries'].append(injury)
            grid_data[team_code]['injury_count'] += 1
    # Sort injuries within each team by reverse chronological order
    for team_code in grid_data:
        if grid_data[team_code]['injuries']:
            grid_data[team_code]['injuries'] = sort_injuries_by_date(grid_data[team_code]['injuries'])
    # Create flat list of all teams sorted alphabetically
    all_teams = []
    for team_code, team_data in grid_data.items():
        all_teams.append({'code': team_code, **team_data})
    all_teams.sort(key=lambda x: x['name'])
    return all_teams

def update_injury_data():
    """Update injury data from sources."""
    global injury_data
    print(f"🔄 Updating injury data at {datetime.now()}")
    try:
        injuries = scrape_hockey_reference_injuries()
        # Organize by team
        by_team = {}
        for injury in injuries:
            team = injury.get('team', 'UNK')
            if team not in by_team:
                by_team[team] = []
            by_team[team].append(injury)
        # Sort injuries by team in reverse chronological order
        for team in by_team:
            by_team[team] = sort_injuries_by_date(by_team[team])
        # Update global data
        injury_data = {
            'injuries': injuries,
            'last_updated': datetime.now().isoformat(),
            'total_count': len(injuries),
            'by_team': by_team,
            'formatted_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        # Create compact team grid
        injury_data['team_grid'] = create_team_grid_with_injuries()
        print(f"✅ Updated with {len(injuries)} injuries")
    except Exception as e:
        print(f"❌ Error updating injury data: {e}")
        if 'injuries' not in injury_data:
            injury_data['injuries'] = []
        injury_data['team_grid'] = create_team_grid_with_injuries()

def schedule_updates():
    """Background thread for scheduled updates."""
    schedule.every().hour.do(update_injury_data)
    while True:
        schedule.run_pending()
        time.sleep(60)

@app.route('/')
def index():
    """Main page showing compact injury team grid."""
    return render_template('injuries.html', data=injury_data)

@app.route('/api/injuries')
def api_injuries():
    """API endpoint for raw injury data."""
    return jsonify(injury_data)

@app.route('/api/refresh')
def api_refresh():
    """Manual refresh endpoint."""
    update_injury_data()
    return jsonify({'status': 'updated', 'timestamp': injury_data['last_updated']})

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'last_updated': injury_data['last_updated'], 'injury_count': injury_data['total_count']})

if __name__ == '__main__':
    print("🚀 Starting NHL Injury Feed Web App...")
    update_injury_data()
    scheduler_thread = Thread(target=schedule_updates, daemon=True)
    scheduler_thread.start()
    print("🌐 Web app starting on http://localhost:5000")
    print("📱 Auto-refresh every hour")
    print("🔄 Manual refresh: http://localhost:5000/api/refresh")
    app.run(host='0.0.0.0', port=5000, debug=False)
