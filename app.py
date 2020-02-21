from flask import Flask, jsonify, request
from controllers.auth import signup_ctrl, login_ctrl

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def signup():
  payload = request.get_json()
  response = signup_ctrl(payload)
  return response


@app.route('/login', methods=['POST'])
def login():
  payload = request.get_json()
  response = login_ctrl(payload)
  return response


@app.errorhandler(404)
def not_found(error):
  return jsonify(error), 404