import os
from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends, Cookie, Request, WebSocket
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

from schemas import User
import db


load_dotenv()
SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']
ACCESS_TOKEN_EXPIRES_MINUTES = int(os.environ['ACCESS_TOKEN_EXPIRES_MINUTES'])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(pool, username: str, password: str):
    user = await db.get_user_by_username(pool, username)
    if not user:
        user = await db.create_user(pool, username, pwd_context.hash(password))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        else:
            return user
    if not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


async def verify_user(pool, token: str) -> User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await db.get_user_by_username(pool, username)
    if not user:
        raise credentials_exception
    return user


async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)) -> User:
    pool = request.app.state.pool
    return await verify_user(pool, token)


async def get_websocket_user(websocket: WebSocket, token: str = Cookie()) -> User:
    pool = websocket.app.state.pool
    return await verify_user(pool, token)
