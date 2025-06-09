# login/utils.py
import jwt
from datetime import datetime, timedelta
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'
TOKEN_LIFETIME_DAYS = 3650  # 10 years for "never expire" unless logout

def create_admin_jwt(user_id,user_name,role):
    payload = {
        'user_id': user_id,
        'user_name':user_name,
        'role': role,
        'iat': datetime.utcnow()
    }
    print("payload", payload)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_admin_jwt(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.InvalidTokenError:
        return None
