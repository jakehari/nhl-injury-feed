from flask import Flask, jsonify
from simple_injury_scraper import scrape_hockey_reference_injuries
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # Get REAL injury data from Hockey Reference
    injuries = scrape_hockey_reference_injuries()

    injuries_html = ""
    for injury in injuries:
        injuries_html += f"<li><strong>{injury['player']}</strong> ({injury['team']}): {injury['injury_type']}"
        if injury['injury_date']:
            injuries_html += f" - {injury['injury_date']}"
        injuries_html += "</li>"

    return f"""
    <h1>🏒 NHL Injury Feed</h1>
    <p><strong>Total Injuries: {len(injuries)}</strong></p>
    <p><strong>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong></p>
    <p><em>Live data from Hockey-Reference.com</em></p>
    <ul>
        {injuries_html}
    </ul>
    <p><a href="/api/injuries">View JSON Data</a></p>
    """

@app.route('/api/injuries')
def api_injuries():
    injuries = scrape_hockey_reference_injuries()
    return jsonify({
        'total_count': len(injuries),
        'injuries': injuries,
        'last_updated': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
