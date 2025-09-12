import requests
from datetime import datetime
import json

def get_nhl_team_info():
    """Get all NHL teams with logos and info."""
    teams = {
        'ANA': {'name': 'Anaheim Ducks', 'logo': '🦆', 'conference': 'Western', 'division': 'Pacific'},
        'BOS': {'name': 'Boston Bruins', 'logo': '🐻', 'conference': 'Eastern', 'division': 'Atlantic'},
        'BUF': {'name': 'Buffalo Sabres', 'logo': '⚔️', 'conference': 'Eastern', 'division': 'Atlantic'},
        'CGY': {'name': 'Calgary Flames', 'logo': '🔥', 'conference': 'Western', 'division': 'Pacific'},
        'CAR': {'name': 'Carolina Hurricanes', 'logo': '🌀', 'conference': 'Eastern', 'division': 'Metropolitan'},
        'CHI': {'name': 'Chicago Blackhawks', 'logo': '🪶', 'conference': 'Western', 'division': 'Central'},
        'COL': {'name': 'Colorado Avalanche', 'logo': '🏔️', 'conference': 'Western', 'division': 'Central'},
        'CBJ': {'name': 'Columbus Blue Jackets', 'logo': '🧥', 'conference': 'Eastern', 'division': 'Metropolitan'},
        'DAL': {'name': 'Dallas Stars', 'logo': '⭐', 'conference': 'Western', 'division': 'Central'},
        'DET': {'name': 'Detroit Red Wings', 'logo': '🪽', 'conference': 'Eastern', 'division': 'Atlantic'},
        'EDM': {'name': 'Edmonton Oilers', 'logo': '🛢️', 'conference': 'Western', 'division': 'Pacific'},
        'FLA': {'name': 'Florida Panthers', 'logo': '🐾', 'conference': 'Eastern', 'division': 'Atlantic'},
        'LAK': {'name': 'Los Angeles Kings', 'logo': '👑', 'conference': 'Western', 'division': 'Pacific'},
        'MIN': {'name': 'Minnesota Wild', 'logo': '🌲', 'conference': 'Western', 'division': 'Central'},
        'MTL': {'name': 'Montreal Canadiens', 'logo': '🇨🇦', 'conference': 'Eastern', 'division': 'Atlantic'},
        'NSH': {'name': 'Nashville Predators', 'logo': '🎸', 'conference': 'Western', 'division': 'Central'},
        'NJD': {'name': 'New Jersey Devils', 'logo': '😈', 'conference': 'Eastern', 'division': 'Metropolitan'},
        'NYI': {'name': 'New York Islanders', 'logo': '🏝️', 'conference': 'Eastern', 'division': 'Metropolitan'},
        'NYR': {'name': 'New York Rangers', 'logo': '🗽', 'conference': 'Eastern', 'division': 'Metropolitan'},
        'OTT': {'name': 'Ottawa Senators', 'logo': '🏛️', 'conference': 'Eastern', 'division': 'Atlantic'},
        'PHI': {'name': 'Philadelphia Flyers', 'logo': '🧡', 'conference': 'Eastern', 'division': 'Metropolitan'},
        'PIT': {'name': 'Pittsburgh Penguins', 'logo': '🐧', 'conference': 'Eastern', 'division': 'Metropolitan'},
        'SJS': {'name': 'San Jose Sharks', 'logo': '🦈', 'conference': 'Western', 'division': 'Pacific'},
        'SEA': {'name': 'Seattle Kraken', 'logo': '🐙', 'conference': 'Western', 'division': 'Pacific'},
        'STL': {'name': 'St. Louis Blues', 'logo': '🎵', 'conference': 'Western', 'division': 'Central'},
        'TBL': {'name': 'Tampa Bay Lightning', 'logo': '⚡', 'conference': 'Eastern', 'division': 'Atlantic'},
        'TOR': {'name': 'Toronto Maple Leafs', 'logo': '🍁', 'conference': 'Eastern', 'division': 'Atlantic'},
        'UTA': {'name': 'Utah Hockey Club', 'logo': '🏔️', 'conference': 'Western', 'division': 'Central'},
        'VAN': {'name': 'Vancouver Canucks', 'logo': '🌊', 'conference': 'Western', 'division': 'Pacific'},
        'VGK': {'name': 'Vegas Golden Knights', 'logo': '⚜️', 'conference': 'Western', 'division': 'Pacific'},
        'WSH': {'name': 'Washington Capitals', 'logo': '🏛️', 'conference': 'Eastern', 'division': 'Metropolitan'},
        'WPG': {'name': 'Winnipeg Jets', 'logo': '✈️', 'conference': 'Western', 'division': 'Central'}
    }
    return teams


def detect_possible_injuries():
    """Detect possible injuries based on reduced ice time (mock implementation)."""
    possible_injuries = [
        {'player': 'Connor McDavid', 'team': 'EDM', 'avg_ice_time': '22:15', 'last_game_ice_time': '14:32', 'difference': '-7:43', 'game_date': '2025-09-11', 'flag_reason': 'Ice time 35% below average', 'confidence': 'High', 'source': 'NHL Stats API', 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
        {'player': 'Auston Matthews', 'team': 'TOR', 'avg_ice_time': '20:48', 'last_game_ice_time': '12:15', 'difference': '-8:33', 'game_date': '2025-09-11', 'flag_reason': 'Ice time 41% below average', 'confidence': 'High', 'source': 'NHL Stats API', 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
        {'player': 'Nathan MacKinnon', 'team': 'COL', 'avg_ice_time': '21:30', 'last_game_ice_time': '16:45', 'difference': '-4:45', 'game_date': '2025-09-10', 'flag_reason': 'Ice time 22% below average', 'confidence': 'Medium', 'source': 'NHL Stats API', 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ]
    return possible_injuries


def get_nhl_api_setup_info():
    """Instructions for setting up NHL Stats API for real ice time tracking."""
    return {
        'api_endpoint': 'https://statsapi.web.nhl.com/api/v1/',
        'documentation': 'https://gitlab.com/dword4/nhlapi',
        'key_endpoints': {
            'teams': '/api/v1/teams',
            'player_stats': '/api/v1/people/{playerId}/stats',
            'game_data': '/api/v1/game/{gameId}/boxscore',
            'schedule': '/api/v1/schedule'
        },
        'ice_time_detection': {
            'method': 'Compare recent game ice time to season average',
            'threshold': 'Flag if >20% reduction in ice time',
            'confidence_levels': {
                'High': '>35% reduction',
                'Medium': '20-35% reduction',
                'Low': '15-20% reduction'
            }
        },
        'update_frequency': 'After each game (daily during season)'
    }
