import jwt
from flask import current_app


def encode(payload):
    print (payload)
    token=jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256')
    print (token)
    return token


def decode(token):
    return jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
