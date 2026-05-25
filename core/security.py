from bcrypt import gensalt, checkpw, hashpw 
from jose import jwt
from core.config import JWT_SECRET_KEY
from datetime import datetime, timezone, timedelta

ALGORITHM="HS256"

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = gensalt(12)
    hashed_password = hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return checkpw(password_bytes, hashed_password_bytes)


def create_access_token(user_id: str, email: str, expiry: int = 60) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expiry)
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expire
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_access_token(token: str):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
    return payload
