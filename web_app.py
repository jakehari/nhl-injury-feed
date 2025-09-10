#!/usr/bin/env python3

  from flask import Flask, render_template, jsonify
  import json
  import os
  from datetime import datetime, timedelta
  from threading import Thread
  import time
  import schedule
  from simple_injury_scraper import scrape_hockey_reference_injuries,
  format_injury_report

  app = Flask(__name__)

  injury_data = {
      'injuries': [],
      'last_updated': None,
      'total_count': 0,
      'by_team': {}
  }

  def update_injury_data():
      global injury_data

      print(f"Updating injury data at {datetime.now()}")

      try:
          injuries = scrape_hockey_reference_injuries()

          by_team = {}
          for injury in injuries:
              team = injury['team']
              if team not in by_team:
                  by_team[team] = []
              by_team[team].append(injury)

          injury_data = {
              'injuries': injuries,
              'last_updated': datetime.now().isoformat(),
              'total_count': len(injuries),
              'by_team': by_team,
              'formatted_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
          }

          print(f"Updated with {len(injuries)} injuries")

      except Exception as e: