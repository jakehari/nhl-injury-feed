#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NHL Injury Feed Web Application
Serves injury data on a webpage with compact team grid layout
"""

from flask import Flask, render_template, jsonify
import json
import os
import requests
from datetime import datetime, timedelta
from threading import Thread
import time
import schedule
from simple_injury_scraper import scrape_hockey_reference_injuries

app = Flask(__name__)

# Global data storage
injury_data = {
    'injuries': [],
    'possible_injuries': [],
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
    'Anaheim Ducks': 'ANA',
    'Boston Bruins': 'BOS',
    'Buffalo Sabres': 'BUF',
    'Calgary Flames': 'CGY',
    'Carolina Hurricanes': 'CAR',
    'Chicago Blackhawks': 'CHI',
    'Colorado Avalanche': 'COL',
    'Columbus Blue Jackets': 'CBJ',
    'Dallas Stars': 'DAL',
    'Detroit Red Wings': 'DET',
    'Edmonton Oilers': 'EDM',
    'Florida Panthers': 'FLA',
    'Los Angeles Kings': 'LAK',
    'Minnesota Wild': 'MIN',
    'Montreal Canadiens': 'MTL',
    'Nashville Predators': 'NSH',
    'New Jersey Devils': 'NJD',
    'New York Islanders': 'NYI',
    'New York Rangers': 'NYR',
    'Ottawa Senators': 'OTT',
    'Philadelphia Flyers': 'PHI',
    'Pittsburgh Penguins': 'PIT',
    'San Jose Sharks': 'SJS',
    'Seattle Kraken': 'SEA',
    'St. Louis Blues': 'STL',
    'Tampa Bay Lightning': 'TBL',
    'Toronto Maple Leafs': 'TOR',
    'Utah Hockey Club': 'UTA',
    'Vancouver Canucks': 'VAN',
    'Vegas Golden Knights': 'VGK',
    'Washington Capitals': 'WSH',
    'Winnipeg Jets': 'WPG'
}

def get_team_id_from_code(team_code):
    """Convert team code to NHL API team ID"""
    team_id_mapping = {
        'ANA': 24, 'BOS': 6, 'BUF': 7, 'CGY': 20, 'CAR': 12, 'CHI': 16, 'COL': 21,
        'CBJ': 29, 'DAL': 25, 'DET': 17, 'EDM': 22, 'FLA': 13, 'LAK': 26, 'MIN': 30,
        'MTL': 8, 'NSH': 18, 'NJD': 1, 'NYI': 2, 'NYR': 3, 'OTT': 9, 'PHI': 4,
        'PIT': 5, 'SJS': 28, 'SEA': 55, 'STL': 19, 'TBL': 14, 'TOR': 10, 'UTA': 53,
        'VAN': 23, 'VGK': 54, 'WSH': 15, 'WPG': 52
    }
    return team_id_mapping.get(team_code)

def analyze_ice_time_for_possible_injuries():
    """Analyze recent games for unusual ice time drops that might indicate injury"""
    possible_injuries = []
    
    try:
        # Get today's date and look back a few days
        today = datetime.now()
        
        for team_code in NHL_TEAMS.keys():
            team_id = get_team_id_from_code(team_code)
            if not team_id:
                continue
            
            # Get recent games for this team
            schedule_url = f"https://api-web.nhle.com/v1/club-schedule-season/{team_id}/20242025"
            
            try:
                response = requests.get(schedule_url, timeout=10)
                if response.status_code == 200:
                    schedule_data = response.json()
                    
                    # Find recent completed games
                    recent_games = []
                    for game in schedule_data.get('games', []):
                        game_date = datetime.strptime(game.get('gameDate', ''), '%Y-%m-%d')
                        if game.get('gameState') == 'OFF' and game_date >= today - timedelta(days=7):
                            recent_games.append(game)
                    
                    # Sort by most recent first
                    recent_games.sort(key=lambda x: x.get('gameDate', ''), reverse=True)
                    
                    if len(recent_games) >= 2:
                        # Analyze the most recent game
                        latest_game = recent_games[0]
                        game_id = latest_game.get('id')
                        
                        if game_id:
                            # Get detailed game stats
                            game_url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore"
                            game_response = requests.get(game_url, timeout=10)
                            
                            if game_response.status_code == 200:
                                game_data = game_response.json()
                                
                                # Analyze players' ice time
                                team_stats = None
                                if game_data.get('homeTeam', {}).get('id') == team_id:
                                    team_stats = game_data.get('homeTeam', {})
                                elif game_data.get('awayTeam', {}).get('id') == team_id:
                                    team_stats = game_data.get('awayTeam', {})
                                
                                if team_stats:
                                    forwards = team_stats.get('forwards', [])
                                    defensemen = team_stats.get('defensemen', [])
                                    all_players = forwards + defensemen
                                    
                                    for player in all_players:
                                        ice_time_str = player.get('toi', '0:00')
                                        if ':' in ice_time_str:
                                            minutes, seconds = ice_time_str.split(':')
                                            ice_time_minutes = int(minutes) + int(seconds) / 60
                                            
                                            # Flag players with unusually low ice time
                                            # These thresholds can be adjusted
                                            position = 'F' if player in forwards else 'D'
                                            min_threshold = 12 if position == 'F' else 15  # Minutes
                                            
                                            # Only flag if they played but very little
                                            if 0 < ice_time_minutes < min_threshold:
                                                possible_injury = {
                                                    'player': player.get('name', {}).get('default', 'Unknown'),
                                                    'team': team_code,
                                                    'ice_time': ice_time_str,
                                                    'position': position,
                                                    'game_date': latest_game.get('gameDate'),
                                                    'reason': f'Low ice time ({ice_time_str}) for {position}',
                                                    'confidence': 'Medium',
                                                    'type': 'possible',
                                                    'source': 'Ice Time Analysis'
                                                }
                                                possible_injuries.append(possible_injury)
                                                print(f"⚠️ Possible injury: {possible_injury['player']} ({team_code}) - {ice_time_str}")
            
            except Exception as e:
                print(f"Error analyzing {team_code}: {e}")
                continue
    
    except Exception as e:
        print(f"Error in ice time analysis: {e}")
    
    return possible_injuries

def sort_injuries_by_date(injuries):
    """Sort injuries in reverse chronological order"""
    def get_sort_key(injury):
        injury_date = injury.get('injury_date', '')
        scraped_at = injury.get('scraped_at', '')
        game_date = injury.get('game_date', '')
        
        for date_str in [injury_date, scraped_at, game_date]:
            if date_str:
                try:
                    if 'T' in date_str:
                        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    else:
                        return datetime.strptime(date_str, '%Y-%m-%d')
                except (ValueError, TypeError):
                    continue
        
        return datetime.now()
    
    return sorted(injuries, key=get_sort_key, reverse=True)

def create_team_grid_with_injuries():
    """Create compact team grid with both confirmed and possible injuries"""
    grid_data = {}
    
    for team_code, team_info in NHL_TEAMS.items():
        grid_data[team_code] = {
            'name': team_info['name'],
            'logo': team_info['logo'],
            'division': team_info['division'],
            'confirmed_injuries': [],
            'possible_injuries': [],
            'injury_count': 0,
            'possible_count': 0
        }
    
    # Add confirmed injuries
    for injury in injury_data['injuries']:
        team_name = injury.get('team', '').strip()
        team_code = TEAM_NAME_TO_CODE.get(team_name, team_name.upper())
        if team_code in grid_data:
            injury['type'] = 'confirmed'
            grid_data[team_code]['confirmed_injuries'].append(injury)
            grid_data[team_code]['injury_count'] += 1
    
    # Add possible injuries
    for injury in injury_data['possible_injuries']:
        team_code = injury.get('team', '').strip()
        if team_code in grid_data:
            injury['type'] = 'possible'
            grid_data[team_code]['possible_injuries'].append(injury)
            grid_data[team_code]['possible_count'] += 1
    
    # Sort injuries within each team
    for team_code in grid_data:
        if grid_data[team_code]['confirmed_injuries']:
            grid_data[team_code]['confirmed_injuries'] = sort_injuries_by_date(grid_data[team_code]['confirmed_injuries'])
        if grid_data[team_code]['possible_injuries']:
            grid_data[team_code]['possible_injuries'] = sort_injuries_by_date(grid_data[team_code]['possible_injuries'])
    
    all_teams = []
    for team_code, team_data in grid_data.items():
        all_teams.append({
            'code': team_code,
            **team_data
        })
    
    all_teams.sort(key=lambda x: x['name'])
    
    return all_teams

def update_injury_data():
    """Update injury data including ice time analysis"""
    global injury_data
    
    print(f"Updating injury data at {datetime.now()}")
    
    try:
        # Get confirmed injuries from scraper
        injuries = scrape_hockey_reference_injuries()
        
        # Get possible injuries from ice time analysis
        print("🔍 Analyzing ice time for possible injuries...")
        possible_injuries = analyze_ice_time_for_possible_injuries()
        
        # Process confirmed injuries by team
        by_team = {}
        for injury in injuries:
            team = injury['team']
            if team not in by_team:
                by_team[team] = []
            by_team[team].append(injury)
        
        for team in by_team:
            by_team[team] = sort_injuries_by_date(by_team[team])
        
        # Update global data
        injury_data = {
            'injuries': injuries,
            'possible_injuries': possible_injuries,
            'last_updated': datetime.now().isoformat(),
            'total_count': len(injuries),
            'possible_count': len(possible_injuries),
            'by_team': by_team,
            'formatted_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        injury_data['team_grid'] = create_team_grid_with_injuries()
        
        print(f"✅ Updated with {len(injuries)} confirmed injuries and {len(possible_injuries)} possible injuries")
    
    except Exception as e:
        print(f"Error updating injury data: {e}")
        if 'injuries' not in injury_data:
            injury_data['injuries'] = []
        if 'possible_injuries' not in injury_data:
            injury_data['possible_injuries'] = []
        injury_data['team_grid'] = create_team_grid_with_injuries()

def schedule_updates():
    """Background thread for updates"""
    schedule.every().hour.do(update_injury_data)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

@app.route('/')
def index():
    """Main page"""
    return render_template('injuries.html', data=injury_data)

@app.route('/api/injuries')
def api_injuries():
    """API endpoint"""
    return jsonify(injury_data)

@app.route('/api/refresh')
def api_refresh():
    """Manual refresh"""
    update_injury_data()
    return jsonify({'status': 'updated', 'timestamp': injury_data['last_updated']})

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'last_updated': injury_data['last_updated'],
        'injury_count': injury_data['total_count'],
        'possible_count': injury_data.get('possible_count', 0)
    })

if __name__ == '__main__':
    print("Starting NHL Injury Feed Web App...")
    update_injury_data()
    
    scheduler_thread = Thread(target=schedule_updates, daemon=True)
    scheduler_thread.start()
    
    print("Web app starting on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)