from flask import Flask 
from flask import Flask, render_template, jsonify
app = Flask(__name__)

@app.route('/')
def index():
return "<h1>NHL Injury Feed</h1><p>Coming soon...</p>"

if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000)

Step 3: Save and verify

type web_app.py | findstr /n "from flask"