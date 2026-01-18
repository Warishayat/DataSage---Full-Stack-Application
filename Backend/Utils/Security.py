from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status,Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from Core.database import get_supabase
import os

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    supabase = get_supabase()

    try:
        res = supabase.auth.get_user(token)
        return res.user
    except:
        raise HTTPException(
            status_code=401,
            detail="Token is invalid or expired"
        )