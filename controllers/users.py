from flask import Flask, jsonify, request
from models.users import get_user, change_settings as change_settings_mod


def get_settings(email):
    user = get_user(email)
    if not user:
        return jsonify({
            'message': f'No user data for {email}'
        }), 404
    settings = user.get('settings', {})
    return jsonify({
        'payload': settings,
        'message': 'ok'
    }), 200


def change_settings(email):
    user = get_user(email)
    if not user:
        return jsonify({
            'message': f'No user data for {email}'
        }), 404
    response = change_settings_mod(email, request.get_json())
    if not response:
        return jsonify({
            'message': 'could not update settings'
        }), 500
    return jsonify({
        'message': 'ok'
    }), 200

def gen_settings():
    # TODO: do some kind of spread to update a single key and not overwrite
    pass