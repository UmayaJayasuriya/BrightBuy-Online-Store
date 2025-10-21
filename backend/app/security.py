from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required but not set in .env file")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60* 1  # 1 hour


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": now})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


bearer_scheme = HTTPBearer(auto_error=False)  # Changed to False to get better error messages


def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from e


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> Dict[str, Any]:
    if not credentials:
        print("DEBUG: No credentials provided!")
        raise HTTPException(
            status_code=401, 
            detail="Authorization header missing. Please provide a Bearer token."
        )
    print(f"DEBUG: Received credentials: {credentials}")
    token = credentials.credentials
    print(f"DEBUG: Token (first 20 chars): {token[:20]}...")
    payload = decode_token(token)
    print(f"DEBUG: Decoded payload: {payload}")
    # Expected fields: sub (user_id), user_name, email, user_type
    if not payload.get("sub"):
        raise HTTPException(status_code=401, detail="Invalid token: missing subject")
    print(f"DEBUG: User type: {payload.get('user_type')}")
    return payload


def get_admin_user(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    if user.get("user_type") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
