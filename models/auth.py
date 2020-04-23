import bcrypt
import boto3
from jwt import JWT, jwk_from_pem, jwk_from_dict
from models.users import get_user
import time
import json

jwt = JWT()
client = boto3.client('dynamodb')
user_table = 'pleasant_pixel_users'

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
                    'S': str(hashed)
                }
            }
        )
        return True
    except:
        return False

def login_mod(email, password):
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    stored_pw = get_user(email).get('password').get('S').encode('utf-8')
    password_matches = bcrypt.checkpw(stored_pw, hashed)
    print(password_matches)
    if password_matches:
        token = gen_token(email)
        print(token)
        return token
    else:
        return 'Passwords do not match'


def gen_token(email):
    with open('rsa_private_key.pem', 'rb') as fh:
        twentyFourHours = 8.64e7
        signing_key = jwk_from_pem(fh.read())
        message = {
            'sub': email,
            'iat': time.time() * 100,
            'exp': time.time() * 100 + twentyFourHours
        }
        compact_jws = jwt.encode(message, signing_key, 'RS256')
        print(compact_jws)
        return compact_jws


def check_token(compact_jws, email):
    with open('rsa_public_key.json', 'r') as fh:
        verifying_key = jwk_from_dict(json.load(fh))
        message_received = jwt.decode(compact_jws, verifying_key)
        is_expired = time.time() * 100 - message_received.exp < 0
        emails_do_not_match = message_received.sub != email
        if is_expired or emails_do_not_match:
            return False
        else:
            return True
