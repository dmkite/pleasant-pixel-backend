from flask import Flask, jsonify, request
from controllers.auth import signup_controller

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def signup():
  payload = request.get_json()
  response = signup_controller(payload)
  return response

@app.errorhandler(404)
def not_found(error):
  return jsonify(error), 404