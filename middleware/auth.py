from flask import request, jsonify
import jwt
import time
import math

key = 'secret'


def authenticate(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization').split()[1]
        decoded = jwt.decode(token, key, algorithms='HS256')
        print(decoded)
        print(time.time() * 100)
        is_expired = decoded.get('exp', math.inf) < (time.time() * 100)
        print(is_expired)
        if is_expired:
            return jsonify({'message': 'expired token'}), 401
        return func(*args, **kwargs)
    return wrapper
