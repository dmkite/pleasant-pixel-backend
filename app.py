from flask import Flask, jsonify, request
from controllers.auth import signup_ctrl, login_ctrl
from middleware.auth import authenticate
from controllers.users import get_settings, change_settings
from controllers.calendar import get_calendar, update_day

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


@app.route('/users/<email>/settings', methods=['GET', 'PUT'])
@authenticate
def settings(email):
    if request.method == 'GET':
        settings = get_settings(email)
        return settings
    else:
        return change_settings(email)


@app.route('/users/<email>/calendar', methods=['GET'])
@authenticate
def calendar(email):
    if not email:
        return jsonify({'message': 'You must provide an email'}), 400
    else:
        return get_calendar(email)


@app.route('/users/<email>/calendar/<year>', methods=['GET'])
@authenticate
def get_year(email, year):
    if not email:
        return jsonify({'message': 'You must provide an email'}), 400
    else:
        return get_calendar(email, year=year)


# @app.route(
#     '/users/<email>/calendar/<year>',
#     # defaults={'email': None,'year': None, 'month': None, 'day': None},
#     methods=['GET', 'PUT'])
# # @authenticate
# def calendar(email, year, month, day):
#     print(email, year, month, day)
#     if not email:
#         return jsonify({'message': 'You must provide an email'}), 400
#     if request.method == 'GET':
#         return get_calendar(email, year, month, day)
#     else:
#         return update_day(email, year, month, day)


@app.route(
    '/users/<email>/calendar/<year>/<month>/<day>',
    methods=['GET', 'PUT'])
# @authenticate
def calendar_day(email, year, month, day):
    print(email, year, month, day)
    if not email:
        return jsonify({'message': 'You must provide an email'}), 400
    if request.method == 'GET':
        return get_calendar(email, year=year, month=month, day=day)
    else:
        return update_day(email, year, month, day, request.get_json())


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'message': f'We couldn\'t find that endpoint: {e}'
    }), 404
