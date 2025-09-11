  from flask import Flask, render_template, jsonify
  app = Flask(__name__)

  @app.route('/')
  def index():
      return "<h1>NHL Injury Feed</h1><p>Coming soon...</p>"

  if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5000)