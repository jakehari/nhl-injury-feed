#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NHL Injury Feed Web Application
Serves injury data on a webpage with compact team grid layout
"""

from flask import Flask, render_template, jsonify
from datetime import datetime
from threading import Thread
import time
import schedule
from simple_injury_scraper import scrape_hockey_reference_injuries

app = Flask(__name__)

# Global data storage
injury_data = {
    'injuries': [],
    'last_updated': None,
    'total_count': 0,
    'by_team': {},
    'team_grid': []
}

# NHL Team Information with simple text logos
NHL_TEAMS = {
    'ANA': {'name': 'Anaheim Ducks', 'logo': 'ANA', 'division': 'Pacific'},
    'BOS': {'name': 'Boston Bruins', 'logo': 'BOS', 'division': 'Atlantic'},
    'BUF': {'name': 'Buffalo Sabres', 'logo': 'BUF', 'division': 'Atlantic'},
    'CGY': {'name': 'Calgary Flames', 'logo': 'CGY', 'division': 'Pacific'},
    'CAR': {'name': 'Carolina Hurricanes', 'logo': 'CAR', 'division': 'Metropolitan'},
    'CHI': {'name': 'Chicago Blackhawks', 'logo': 'CHI', 'division': 'Central'},
    'COL': {'name': 'Colorado Avalanche', 'logo': 'COL', 'division': 'Central'},
    'CBJ': {'name': 'Columbus Blue Jackets', 'logo': 'CBJ', 'division': 'Metropolitan'},
    'DAL': {'name': 'Dallas Stars', 'logo': 'DAL', 'division': 'Central'},
    'DET': {'name': 'Detroit Red Wings', 'logo': 'DET', 'division': 'Atlantic'},
    'EDM': {'name': 'Edmonton Oilers', 'logo': 'EDM', 'division': 'Pacific'},
    'FLA': {'name': 'Florida Panthers', 'logo': 'FLA', 'division': 'Atlantic'},
    'LAK': {'name': 'Los Angeles Kings', 'logo': 'LAK', 'division': 'Pacific'},
    'MIN': {'name': 'Minnesota Wild', 'logo': 'MIN', 'division': 'Central'},
    'MTL': {'name': 'Montreal Canadiens', 'logo': 'MTL', 'division': 'Atlantic'},
    'NSH': {'name': 'Nashville Predators', 'logo': 'NSH', 'division': 'Central'},
    'NJD': {'name': 'New Jersey Devils', 'logo': 'NJD', 'division': 'Metropolitan'},
    'NYI': {'name': 'New York Islanders', 'logo': 'NYI', 'division': 'Metropolitan'},
    'NYR': {'name': 'New York Rangers', 'logo': 'NYR', 'division': 'Metropolitan'},
    'OTT': {'name': 'Ottawa Senators', 'logo': 'OTT', 'division': 'Atlantic'},
    'PHI': {'name': 'Philadelphia Flyers', 'logo': 'PHI', 'division': 'Metropolitan'},
    'PIT': {'name': 'Pittsburgh Penguins', 'logo': 'PIT', 'division': 'Metropolitan'},
    'SJS': {'name': 'San Jose Sharks', 'logo': 'SJS', 'division': 'Pacific'},
    'SEA': {'name': 'Seattle Kraken', 'logo': 'SEA', 'division': 'Pacific'},
    'STL': {'name': 'St. Louis Blues', 'logo': 'STL', 'division': 'Central'},
    'TBL': {'name': 'Tampa Bay Lightning', 'logo': 'TBL', 'division': 'Atlantic'},
    'TOR': {'name': 'Toronto Maple Leafs', 'logo': 'TOR', 'division': 'Atlantic'},
    'UTA': {'name': 'Utah Hockey Club', 'logo': 'UTA', 'division': 'Central'},
    'VAN': {'name': 'Vancouver Canucks', 'logo': 'VAN', 'division': 'Pacific'},
    'VGK': {'name': 'Vegas Golden Knights', 'logo': 'VGK', 'division': 'Pacific'},
    'WSH': {'name': 'Washington Capitals', 'logo': 'WSH', 'division': 'Metropolitan'},
    'WPG': {'name': 'Winnipeg Jets', 'logo': 'WPG', 'division': 'Central'}
}

# Team name mapping
TEAM_NAME_TO_CODE = {
    'Anaheim Ducks': 'ANA', 'Boston Bruins': 'BOS', 'Buffalo Sabres': 'BUF', 'Calgary Flames': 'CGY',
    'Carolina Hurricanes': 'CAR', 'Chicago Blackhawks': 'CHI', 'Colorado Avalanche': 'COL', 'Columbus Blue Jackets': 'CBJ',
    'Dallas Stars': 'DAL', 'Detroit Red Wings': 'DET', 'Edmonton Oilers': 'EDM', 'Florida Panthers': 'FLA',
    'Los Angeles Kings': 'LAK', 'Minnesota Wild': 'MIN', 'Montreal Canadiens': 'MTL', 'Nashville Predators': 'NSH',
    'New Jersey Devils': 'NJD', 'New York Islanders': 'NYI', 'New York Rangers': 'NYR', 'Ottawa Senators': 'OTT',
    'Philadelphia Flyers': 'PHI', 'Pittsburgh Penguins': 'PIT', 'San Jose Sharks': 'SJS', 'Seattle Kraken': 'SEA',
    'St. Louis Blues': 'STL', 'Tampa Bay Lightning': 'TBL', 'Toronto Maple Leafs': 'TOR', 'Utah Hockey Club': 'UTA',
    'Vancouver Canucks': 'VAN', 'Vegas Golden Knights': 'VGK', 'Washington Capitals': 'WSH', 'Winnipeg Jets': 'WPG'
}

def sort_injuries_by_date(injuries):
    """Sort injuries in reverse chronological order."""
    def get_sort_key(injury):
        for date_str in [injury.get('injury_date', ''), injury.get('scraped_at', '')]:
            if date_str:
                try:
                    if 'T' in date_str:
                        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    return datetime.strptime(date_str, '%Y-%m-%d')
                except (ValueError, TypeError):
                    continue
        return datetime.now()
    return sorted(injuries, key=get_sort_key, reverse=True)

def create_team_grid_with_injuries():
    """Create compact team grid with all teams visible."""
    grid_data = {code: {'name': info['name'], 'logo': info['logo'], 'division': info['division'], 'injuries': [], 'injury_count': 0} for code, info in NHL_TEAMS.items()}
    for injury in injury_data['injuries']:
        team_name = injury.get('team', '').strip()
        team_code = TEAM_NAME_TO_CODE.get(team_name, team_name.upper())
        print(f"Processing: {injury.get('player')} - {team_name} -> {team_code}")
        if team_code in grid_data:
            grid_data[team_code]['injuries'].append(injury)
            grid_data[team_code]['injury_count'] += 1
            print(f"Added to {team_code}: {injury.get('player')}")
        else:
            print(f"Team code {team_code} not found")
    for code in grid_data:
        if grid_data[code]['injuries']:
            grid_data[code]['injuries'] = sort_injuries_by_date(grid_data[code]['injuries'])
    all_teams = [{'code': code, **data} for code, data in grid_data.items()]
    all_teams.sort(key=lambda x: x['name'])
    return all_teams

def update_injury_data():
    """Update injury data."""
    global injury_data
    print(f"Updating injury data at {datetime.now()}")
    try:
        injuries = scrape_hockey_reference_injuries()
        by_team = {}
        for injury in injuries:
            by_team.setdefault(injury['team'], []).append(injury)
        for team in by_team:
            by_team[team] = sort_injuries_by_date(by_team[team])
        injury_data = {
            'injuries': injuries,
            'last_updated': datetime.now().isoformat(),
            'total_count': len(injuries),
            'by_team': by_team,
            'formatted_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        injury_data['team_grid'] = create_team_grid_with_injuries()
        print(f"Updated with {len(injuries)} injuries")
    except Exception as e:
        print(f"Error updating injury data: {e}")
        if 'injuries' not in injury_data:
            injury_data['injuries'] = []
        injury_data['team_grid'] = create_team_grid_with_injuries()

def schedule_updates():
    """Background thread for updates."""
    schedule.every().hour.do(update_injury_data)
    while True:
        schedule.run_pending()
        time.sleep(60)

@app.route('/')
def index():
    return render_template('injuries.html', data=injury_data)

@app.route('/api/injuries')
def api_injuries():
    return jsonify(injury_data)

@app.route('/api/refresh')
def api_refresh():
    update_injury_data()
    return jsonify({'status': 'updated', 'timestamp': injury_data['last_updated']})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'last_updated': injury_data['last_updated'], 'injury_count': injury_data['total_count']})

if __name__ == '__main__':
    print("Starting NHL Injury Feed Web App...")
    update_injury_data()
    scheduler_thread = Thread(target=schedule_updates, daemon=True)
    scheduler_thread.start()
    print("Web app starting on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
