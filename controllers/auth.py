from flask import jsonify

def signup_controller(payload={}):
    if 'email' not in payload or 'password' not in payload or 'passwordMatch' not in payload:
        return jsonify('Missing information'), 400
    if payload['password'] != payload['passwordMatch']:
        return jsonify('Passwords do not match'), 400
    return jsonify('Looking good'), 200
    
