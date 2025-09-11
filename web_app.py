from flask import Flask, render_template, jsonify
import json
from datetime import datetime
from threading import Thread
import time
import schedule
from simple_injury_scraper import scrape_hockey_reference_injuries

app = Flask(__name__)

injury_data = {
    'injuries': [],
    'last_updated': None,
    'total_count': 0,
    'by_team': {},
    'formatted_time': None
}