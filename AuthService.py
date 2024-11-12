import datetime
import hashlib

import jwt

from config import SECRET_KEY


class AuthService:

    @staticmethod
    def create_jwt(data, expires_in):
        payload = data.copy()
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_jwt(token):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
