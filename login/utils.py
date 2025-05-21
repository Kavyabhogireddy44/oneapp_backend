# login/utils.py
import jwt
from datetime import datetime, timedelta
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'
TOKEN_LIFETIME_DAYS = 3650  # 10 years for "never expire" unless logout

def create_jwt(user_id, phone, user_name):
    payload = {
        'user_id': user_id,
        'phone': phone,
        'user_name':user_name,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.InvalidTokenError:
        return None
