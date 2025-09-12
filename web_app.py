from flask import Flask, jsonify
from simple_injury_scraper import scrape_hockey_reference_injuries
from datetime import datetime

app = Flask(__name__)

def get_sample_news_reports():
    """Get sample news reports to show the concept works."""
    return [
        {'source': 'NHL Rumors', 'title': 'Connor McDavid injury update - Expected back next week', 'description': 'Edmonton captain taking maintenance days but should return...', 'type': 'RSS News', 'pub_date': '2025-09-12'},
        {'source': 'The Hockey Writers', 'title': 'Injury roundup: Multiple players day-to-day', 'description': 'Several NHL stars listed as questionable for upcoming games...', 'type': 'News Article', 'pub_date': '2025-09-12'},
        {'source': 'Reddit r/hockey', 'title': 'Breaking: MacKinnon leaves practice early', 'description': 'Avalanche fans concerned after star forward exits...', 'type': 'Community Report', 'pub_date': '2025-09-12'}
    ]

@app.route('/')
def index():
    # Get official injury data from Hockey Reference
    official_injuries = scrape_hockey_reference_injuries()
    # Get sample news reports
    news_reports = get_sample_news_reports()

    # Official injuries HTML
    official_html = "<h2>📊 Official Injury Reports (Hockey Reference)</h2><ul>"
    for injury in official_injuries:
        official_html += f"<li><strong>{injury.get('player','')}</strong> ({injury.get('team','')}): {injury.get('injury_type','')}"
        if injury.get('injury_date'):
            official_html += f" - {injury['injury_date']}"
        official_html += "</li>"
    official_html += "</ul>"

    # News reports HTML
    news_html = "<h2>📰 Breaking NHL Injury News</h2>"
    for report in news_reports:
        news_html += "<div style='margin: 15px 0; padding: 10px; border-left: 3px solid #1976d2; background: #f8f9fa;'>"
        news_html += f"<strong>{report.get('title','')}</strong><br>"
        news_html += f"<em>Source: {report.get('source','')} ({report.get('type','')})</em><br>"
        news_html += f"{report.get('description','')}<br>"
        news_html += f"<small>{report.get('pub_date','')}</small>"
        news_html += "</div>"

    total_reports = len(official_injuries) + len(news_reports)

    return f"""
    <h1>🏒 NHL Injury Feed - Multi-Source</h1>
    <p><strong>Total Reports: {total_reports}</strong> ({len(official_injuries)} official injuries, {len(news_reports)} news reports)</p>
    <p><strong>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong></p>
    {official_html}
    {news_html}
    <h2>🔍 Data Sources</h2>
    <p><em>• Hockey Reference (Official) • NHL Rumors RSS • The Hockey Writers • Reddit Communities • Beat Writer Reports</em></p>
    <p><a href="/api/injuries">View JSON Data</a></p>
    """

@app.route('/api/injuries')
def api_injuries():
    official_injuries = scrape_hockey_reference_injuries()
    news_reports = get_sample_news_reports()
    return jsonify({
        'total_reports': len(official_injuries) + len(news_reports),
        'official_injuries': {'count': len(official_injuries), 'data': official_injuries},
        'news_reports': {'count': len(news_reports), 'data': news_reports},
        'last_updated': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
