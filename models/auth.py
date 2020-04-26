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
    # password = password.encode('utf-8')
    stored_pw = get_user(email).get('password').get('B')
    password_matches = bcrypt.checkpw(password.encode('utf-8'), stored_pw)

    if password_matches:
        token = gen_token(email)
        print(token)
        return token
    else:
        return 'Passwords do not match'


def gen_token(email):
    twentyFourHours = 8.64e7
    message = {
        'sub': email,
        'iat': time.time() * 100,
        'exp': time.time() * 100 + twentyFourHours
    }
    encoded = jwt.encode(message, key, algorithm='HS256')
    return encoded



def check_token(token, email):
    decoded = jwt.decode(token, key, algorithms='HS256')
    print(decoded)
    # is_expired = time.time() * 100 - message_received.exp < 0
    # emails_do_not_match = message_received.sub != email

