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

# NHL Team Information with simple text logos (no emojis)
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

# Full team name -> code mapping (for when the scraper returns full names)
TEAM_NAME_TO_CODE = {
    'Anaheim Ducks': 'ANA', 'Boston Bruins': 'BOS', 'Buffalo Sabres': 'BUF', 'Calgary Flames': 'CGY',
    'Carolina Hurricanes': 'CAR', 'Chicago Blackhawks': 'CHI', 'Colorado Avalanche': 'COL', 'Columbus Blue Jackets': 'CBJ',
    'Dallas Stars': 'DAL', 'Detroit Red Wings': 'DET', 'Edmonton Oilers': 'EDM', 'Florida Panthers': 'FLA',
    'Los Angeles Kings': 'LAK', 'Minnesota Wild': 'MIN', 'Montreal Canadiens': 'MTL', 'Nashville Predators': 'NSH',
    'New Jersey Devils': 'NJD', 'New York Islanders': 'NYI', 'New York Rangers': 'NYR', 'Ottawa Senators': 'OTT',
    'Philadelphia Flyers': 'PHI', 'Pittsburgh Penguins': 'PIT', 'San Jose Sharks': 'SJS', 'Seattle Kraken': 'SEA',
    'St. Louis Blues': 'STL', 'Tampa Bay Lightning': 'TBL', 'Toronto Maple Leafs': 'TOR', 'Utah Hockey Club': 'UTA',
    'Vancouver Canucks': 'VAN', 'Vegas G
