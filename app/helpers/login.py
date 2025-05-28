from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from app.schemas.login import UserInDB, TokenData, User
from app.db.user import fake_users_db
from loguru import logger

import os 
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

def verify_password(plain_password, hashed_password):
    " Verify a plain password against a hashed password."
    verified =  pwd_context.verify(plain_password, hashed_password)
    logger.debug(f"Password verification result: {verified}")
    return verified

def hash_password(password):
    " Hash a plain password using bcrypt."
    return pwd_context.hash(password)

def get_user(db, username: str):
    " Retrieve a user from the database by username."
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    " Authenticate a user by checking the username and password."
    user = get_user(fake_db, username)
    logger.debug(f"Authenticating user: {username}")
    logger.debug(f"Password provided: {password}")
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    " Create an access token with an expiration time."
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    " Get the current user from the access token."
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.debug(f"Received token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Decoded JWT payload: {payload}")
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, 
                    username=token_data.username)
    logger.debug(f"Current user: {user}")
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    " Ensure the current user is active."
    logger.debug(f"Checking if user {current_user.username} is active")
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user