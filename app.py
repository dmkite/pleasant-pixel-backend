from flask import Flask, jsonify, request
from controllers.auth import signup_ctrl, login_ctrl
from middleware.auth import authenticate
from controllers.users import get_settings, change_settings

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


@app.route('/settings/<email>', methods=['GET', 'PUT'])
@authenticate
def settings(email):
    if request.method == 'GET':
        settings = get_settings(email)
        return settings
    else:
        return change_settings(email)


@app.errorhandler(404)
def not_found():
    return jsonify({
        'message': 'We couldn\'t find that endpoint'
    }), 404
