import bcrypt
import boto3
import jwt
from models.users import get_user
import time
import json

client = boto3.client('dynamodb')
user_table = 'pleasant_pixel_users'
key = 'secret'

def signup_mod(email, password):
    try:
        password = password.encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        client.put_item(
            TableName=user_table,
            Item={
                'email': {
                    'S': email.lower()
                },
                'password': {
                    'B': hashed
                }
            }
        )
        return True
    except:
        return False

def login_mod(email, password):
    user = get_user(email)
    stored_pw = user.get('password', {}).get('B')
    if not stored_pw:
        return f'No record for {email}'
    password_matches = bcrypt.checkpw(password.encode('utf-8'), stored_pw)

    if password_matches:
        token = gen_token(email)
        return token
    else:
        return 'Passwords do not match'


def gen_token(email):
    twentyFourHours = 86400
    message = {
        'sub': email,
        'iat': time.time(),
        'exp': time.time() + twentyFourHours
    }
    encoded = jwt.encode(message, key, algorithm='HS256')
    return encoded



def check_token(token, email):
    decoded = jwt.decode(token, key, algorithms='HS256')
    print(decoded)
    # is_expired = time.time() * 100 - message_received.exp < 0
    # emails_do_not_match = message_received.sub != email

