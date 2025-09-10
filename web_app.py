  #!/usr/bin/env python3
  """
  NHL Injury Feed Web Application
  Serves injury data on a webpage that auto-refreshes every hour
  """

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

  # Global data storage
  injury_data = {
      'injuries': [],
      'last_updated': None,
      'total_count': 0,
      'by_team': {}
  }

  def update_injury_data():
      """Update injury data from sources"""
      global injury_data

      print(f"🔄 Updating injury data at {datetime.now()}")

      try:
          # Get injuries from Hockey Reference
          injuries = scrape_hockey_reference_injuries()

          # Process and organize data
          by_team = {}
          for injury in injuries:
              team = injury['team']
              if team not in by_team:
                  by_team[team] = []
              by_team[team].append(injury)

          # Update global data
          injury_data = {
              'injuries': injuries,
              'last_updated': datetime.now().isoformat(),
              'total_count': len(injuries),
              'by_team': by_team,
              'formatted_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
          }

          print(f"✅ Updated with {len(injuries)} injuries")

      except Exception as e:
          print(f"❌ Error updating injury data: {e}")

  def schedule_updates():
      """Background thread for scheduled updates"""
      schedule.every().hour.do(update_injury_data)

      while True:
          schedule.run_pending()
          time.sleep(60)  # Check every minute

  @app.route('/')
  def index():
      """Main page showing injury feed"""
      return render_template('injuries.html', data=injury_data)

  @app.route('/api/injuries')
  def api_injuries():
      """API endpoint for raw injury data"""
      return jsonify(injury_data)

  @app.route('/api/refresh')
  def api_refresh():
      """Manual refresh endpoint"""
      update_injury_data()
      return jsonify({'status': 'updated', 'timestamp': injury_data['last_updated']})

  @app.route('/health')
  def health():
      """Health check endpoint"""
      return jsonify({
          'status': 'healthy',
          'last_updated': injury_data['last_updated'],
          'injury_count': injury_data['total_count']
      })

  if __name__ == '__main__':
      # Initial data load
      print("🚀 Starting NHL Injury Feed Web App...")
      update_injury_data()

      # Start background scheduler
      scheduler_thread = Thread(target=schedule_updates, daemon=True)
      scheduler_thread.start()

      print("🌐 Web app starting on http://localhost:5000")
      print("📱 Auto-refresh every hour")
      print("🔄 Manual refresh: http://localhost:5000/api/refresh")

      app.run(host='0.0.0.0', port=5000, debug=False)