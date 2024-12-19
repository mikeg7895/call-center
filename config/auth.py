from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "6f2ec29ddc9dd376e1337ff9a81c2bdbf8fcb33ed179b8eb4e5f0ba582f3a52e"
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt