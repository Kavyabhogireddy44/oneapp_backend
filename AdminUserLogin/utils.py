# login/utils.py
import jwt
from datetime import datetime, timedelta
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'
TOKEN_LIFETIME_DAYS = 3650  # 10 years for "never expire" unless logout

def create_admin_jwt(user_id,phone,role):
    payload = {
        'Admin_user_id': user_id,
        'phone': phone,
        'role': role,
        'iat': datetime.utcnow()
    }
    print("payload", payload)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_admin_jwt(token):
    try:
        print("token", token)
        print("SECRET_KEY", SECRET_KEY)
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("decodedmain", decoded)
        return decoded
    except jwt.InvalidTokenError:
        return None
# def verify_admin_jwt(token):
#     try:
#         print("token", token)
#         decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         print("decoded", decoded)
#         return decoded
#     except jwt.ExpiredSignatureError:
#         print("Token expired")
#         return None
#     except jwt.InvalidSignatureError:
#         print("Invalid signature")
#         return None
#     except jwt.DecodeError:
#         print("Decode error")
#         return None
#     except Exception as e:
#         print("Other error:", e)
#         return None
