from app.config.auth import SECRET_KEY, ALGORITHM
from app.schemes.auth_schema import TokenData
from fastapi import HTTPException
from jwt import InvalidTokenError
import jwt

async def get_current_user(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
        username = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(name=username)
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token_data