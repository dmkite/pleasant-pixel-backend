from flask import jsonify
from models.auth import email_already_exists

def signup_controller(payload):
    payload_errors = payload_validation(payload)
    if len(payload_errors) > 0:
        return jsonify(payload_errors), 400
    return jsonify('Looking good'), 200
    
def payload_validation(payload):
    e_validation = entry_validation(payload)
    if len(e_validation) > 0: 
        return e_validation

    validation_errors = []
    if email_already_exists(payload.get('email').strip()):
        validation_errors.append('email is already in use')

    p_validation = password_validation(payload.get('password'))
    if len(p_validation) > 0: 
        validation_errors = validation_errors + p_validation
    return validation_errors

def entry_validation(payload):
    payload_errors = []
    required_fields = ('email', 'password', 'passwordMatch')
    for field in required_fields:
        if payload.get(field) is None:
            payload_errors.append('{} is required'.format(field))
    if payload.get('passwordMatch').strip() != payload.get('password').strip():
        payload_errors.append('passwords do not match')
    return payload_errors

def password_validation(password):
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
    return password_errors
