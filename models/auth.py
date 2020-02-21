import bcrypt 
from jwt import (JWT)
from models.users import get_user

jwt = JWT()

def signup_mod(email, password):
    return True

def login_mod(email, password):
    hashed = bcrypt.hashpw(password, 10)
    stored_pw = get_user(email).password
    if bcrypt.checkpw(stored_pw, hashed):
        return True
    else: 
        return False

def gen_token():
    pass

def check_token():
    pass