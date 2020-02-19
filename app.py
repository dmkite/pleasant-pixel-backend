from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def signup():
  payload = request.get_json()
  return signup(payload)

@app.errorhandler(404)
def not_found(error):
  return jsonify(error), 404