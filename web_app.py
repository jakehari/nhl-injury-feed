from flask import Flask, jsonify
from simple_injury_scraper import scrape_hockey_reference_injuries
from ice_time_monitor import get_nhl_team_info, detect_possible_injuries, get_nhl_api_setup_info
from datetime import datetime

app = Flask(__name__)

def organize_injuries_by_team(injuries):
    """Group injuries by team and sort alphabetically."""
    teams = {}
    for injury in injuries:
        team = injury.get('team', 'UNK')
        if team not in teams:
            teams[team] = []
        injury_with_meta = injury.copy()
        injury_with_meta['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        injury_with_meta['source'] = 'Hockey Reference'
        injury_with_meta['report_type'] = 'Official'
        teams[team].append(injury_with_meta)
    return dict(sorted(teams.items()))

def create_team_overview_grid():
    """Create HTML grid showing all NHL teams."""
    teams_info = get_nhl_team_info()
    html = "<h2>🏒 NHL Teams Overview</h2>"
    html += "<div style='display: grid; grid-template-columns: repeat(8, 1fr); gap: 10px; margin: 20px 0;'>"
    for team_code, team_info in sorted(teams_info.items()):
        html += (
            "<div style='text-align: center; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background: #f9f9f9;'>"
            f"<div style='font-size: 24px;'>{team_info['logo']}</div>"
            f"<div style='font-weight: bold; font-size: 14px;'>{team_code}</div>"
            f"<div style='font-size: 11px; color: #666;'>{team_info['division']}</div>"
            "</div>"
        )
    html += "</div>"
    return html

@app.route('/')
def index():
    # Get all data sources
    official_injuries = scrape_hockey_reference_injuries()
    teams_injuries = organize_injuries_by_team(official_injuries)
    possible_injuries = detect_possible_injuries()

    # Create team overview grid
    team_overview = create_team_overview_grid()

    # Official injuries by team
    official_html = "<h2>📊 Confirmed Injuries (by Team)</h2>"
    for team, injuries in teams_injuries.items():
        official_html += f"<h3>{team}</h3><ul>"
        for injury in injuries:
            official_html += f"<li><strong>{injury.get('player','')}</strong>: {injury.get('injury_type','')}"
            if injury.get('injury_date'):
                official_html += f" ({injury['injury_date']})"
            official_html += f"<br><small>Source: {injury.get('source','')} | Updated: {injury.get('timestamp','')}</small>"
            official_html += "</li>"
        official_html += "</ul>"

    # Possible injuries section
    possible_html = "<h2>⚠️ Possible Injuries (Reduced Ice Time)</h2>"
    if possible_injuries:
        possible_html += "<ul>"
        for injury in possible_injuries:
            possible_html += (
                f"<li><strong>{injury['player']}</strong> ({injury['team']}): "
                f"Avg: {injury['avg_ice_time']} → Last game: {injury['last_game_ice_time']} "
                f"<span style='color: red;'>({injury['difference']})</span><br>"
                f"<small>{injury['flag_reason']} | Confidence: {injury['confidence']} | "
                f"Game: {injury['game_date']} | {injury['timestamp']}</small></li>"
            )
        possible_html += "</ul>"
        possible_html += "<p><em>💡 Tip: Check Twitter manually for these players to confirm potential injuries</em></p>"
    else:
        possible_html += "<p>No significant ice time reductions detected recently.</p>"

    total_official = len(official_injuries)
    total_possible = len(possible_injuries)
    team_count = len(teams_injuries)

    return f"""
    <h1>🏒 NHL Injury Dashboard</h1>
    <p><strong>Total Reports: {total_official + total_possible}</strong> ({total_official} confirmed injuries across {team_count} teams, {total_possible} possible injuries)</p>
    <p><strong>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong></p>
    {team_overview}
    {official_html}
    {possible_html}
    <h2>🔍 Data Sources & Methods</h2>
    <ul>
        <li><strong>Confirmed Injuries:</strong> Hockey Reference (Official injury reports)</li>
        <li><strong>Possible Injuries:</strong> NHL Stats API (Ice time analysis)</li>
        <li><strong>Update Frequency:</strong> Real-time for confirmed, post-game for possible</li>
    </ul>
    <p><a href="/api/injuries">View JSON Data</a> | <a href="/api/nhl-setup">NHL API Setup</a></p>
    """

@app.route('/api/injuries')
def api_injuries():
    official_injuries = scrape_hockey_reference_injuries()
    teams_injuries = organize_injuries_by_team(official_injuries)
    possible_injuries = detect_possible_injuries()
    return jsonify({
        'summary': {
            'total_confirmed': len(official_injuries),
            'total_possible': len(possible_injuries),
            'teams_affected': len(teams_injuries),
            'last_updated': datetime.now().isoformat()
        },
        'confirmed_injuries': {
            'by_team': teams_injuries,
            'source': 'Hockey Reference'
        },
        'possible_injuries': {
            'data': possible_injuries,
            'method': 'Ice time analysis',
            'source': 'NHL Stats API'
        }
    })

@app.route('/api/nhl-setup')
def nhl_setup():
    return jsonify(get_nhl_api_setup_info())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
