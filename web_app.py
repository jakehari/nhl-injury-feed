from flask import Flask, jsonify

app = Flask(__name__)
@app.route('/')
def index():
      return """
      <h1>🏒 NHL Injury Feed</h1>
      <p>Total Injuries: 1</p>
      <h3>NYR (1 injured)</h3>
      <ul>
          <li>Sample Player: Upper Body (2025-09-11)</li>
      </ul>
      <p><a href="/api/injuries">View JSON Data</a></p>
      <p>Last Updated: 2025-09-11 06:30:00</p>
      """

@app.route('/api/injuries')
def api_injuries():
    return jsonify({
        'total_count': 1,
        'injuries': [{'player': 'Sample Player', 'team': 'NYR',
'injury_type': 'Upper Body'}]
    })
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)