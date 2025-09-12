from flask import Flask, jsonify
from simple_injury_scraper import scrape_hockey_reference_injuries
from news_sources_monitor import get_all_news_sources, get_news_source_stats
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    official_injuries = scrape_hockey_reference_injuries()
    news_reports = get_all_news_sources()

    official_html = "<h2>📊 Official Injury Reports</h2><ul>"
    for injury in official_injuries:
        official_html += f"<li><strong>{injury['player']}</strong> ({injury['team']}): {injury['injury_type']}"
        if injury.get('injury_date'):
            official_html += f" - {injury['injury_date']}"
        official_html += "</li>"
    official_html += "</ul>"

    news_html = "<h2>📰 Latest NHL Injury News</h2>"
    for report in news_reports:
        news_html += "<div style='margin: 15px 0; padding: 10px; border-left: 3px solid #1976d2;'>"
        news_html += f"<strong>{report.get('title','')}</strong><br>"
        news_html += f"<em>Source: {report.get('source','')} ({report.get('type','')})</em><br>"
        news_html += f"{report.get('description','')}<br>"
        if report.get('link'):
            news_html += f"<a href='{report['link']}' target='_blank'>Read More</a><br>"
        news_html += f"<small>{report.get('pub_date','')}</small>"
        news_html += "</div>"

    total_reports = len(official_injuries) + len(news_reports)

    return f"""
    <h1>🏒 NHL Injury Feed - Multi-Source</h1>
    <p><strong>Total Reports: {total_reports}</strong> ({len(official_injuries)} official injuries, {len(news_reports)} news reports)</p>
    <p><strong>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong></p>
    {official_html}
    {news_html}
    <h2>🔍 News Sources Monitored</h2>
    <p><em>NHL Rumors RSS • The Hockey Writers RSS • Covers.com • Reddit Communities • Hockey Reference</em></p>
    <p><a href="/api/injuries">View JSON Data</a> | <a href="/api/sources">Source Info</a></p>
    """

@app.route('/api/injuries')
def api_injuries():
    official_injuries = scrape_hockey_reference_injuries()
    news_reports = get_all_news_sources()
    return jsonify({
        'total_reports': len(official_injuries) + len(news_reports),
        'official_injuries': {'count': len(official_injuries), 'data': official_injuries},
        'news_reports': {'count': len(news_reports), 'data': news_reports},
        'last_updated': datetime.now().isoformat()
    })

@app.route('/api/sources')
def api_sources():
    return jsonify(get_news_source_stats())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
