from flask import jsonify
from models.auth import signup_mod, login_mod
from models.users import user_exists

def signup_ctrl(payload):
    payload_errors = payload_validation(payload)
    if len(payload_errors) > 0:
        return jsonify({
            'message': payload_errors
        }), 400
    signup_mod(payload.get('email'), payload.get('password'))
    return jsonify({
        'message': 'ok'
    }), 200


def login_ctrl(payload):
    e_validation = entry_validation(payload, ('email', 'password'))
    if len(e_validation) > 0:
        return jsonify(e_validation), 400
    token = login_mod(payload.get('email'), payload.get('password'))
    if token:
        return jsonify({
            'message': 'ok',
            'token': token.decode('utf-8')
        }), 200
    return jsonify({
        'message': 'Something went wrong.'
    }), 400

    
def payload_validation(payload):
    e_validation = entry_validation(payload, ('email', 'password', 'passwordMatch'))
    if len(e_validation) > 0: 
        return e_validation

    validation_errors = []
    if user_exists(payload.get('email').strip()):
        validation_errors.append('email is already in use')

    p_validation = password_validation(payload.get('password'), payload.get('passwordMatch'))
    if len(p_validation) > 0: 
        validation_errors = validation_errors + p_validation
    return validation_errors


def entry_validation(payload, required_fields):
    payload_errors = []
    for field in required_fields:
        if payload.get(field) is None:
            payload_errors.append(f'{field} is required')
    return payload_errors


def password_validation(password, passwordMatch):
    spec_chars = '!@#$%^&*()-_+=[]{}|;:\'"?/.,><'
    password_errors = []
    if len(password) < 8:
        password_errors.append('password must be at least 8 characters')
    no_caps = True
    no_spec_chars = True
    for char in password:
        if char.upper() == char:
            no_caps = False
        if char in spec_chars:
            no_spec_chars = False
    if no_caps == True:
        password_errors.append('password must include a capital letter')
    if no_spec_chars == True:
        password_errors.append('password must incldue a special character')
    if passwordMatch.strip() != password.strip():
        password_errors.append('passwords do not match')
    return password_errors
