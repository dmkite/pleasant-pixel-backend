from flask import request, jsonify
from functools import wraps
import jwt
import time
import math

key = 'secret'


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        bearer = request.headers.get('Authorization')
        if not bearer: 
            return jsonify({'message': 'no token'}), 401
        token = bearer.split()[1]
        decoded = jwt.decode(token, key, algorithms='HS256')
        print(decoded.get('exp', math.inf))
        is_expired = decoded.get('exp', math.inf) < (time.time())
        if is_expired:
            return jsonify({'message': 'expired token'}), 401
        return func(*args, **kwargs)
    return wrapper

158863083885.0293