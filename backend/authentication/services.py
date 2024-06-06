from typing import Dict
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import jwt, JWTError
from os import getenv
from pydantic import EmailStr

from ..users.services import get_user_by_email
from .. utils.security import verify_hashed_string
from .exceptions import InvalidCredentials
from ..users.services import get_user_by_id


def authenticate_user(db: Session, email: EmailStr, password: str) -> bool:
    """
    Authenticates a user based on his email address and password.

        Parameters:
            db (Session): A database session.
            email (EmailStr): An email address of the user to be authenticated.
            password (str): A password of the user to be authenticated.

        Returns:
            bool: Returns True if authentication succeeds, otherwise False.
    """
    user = get_user_by_email(db, email)
    if user is None:
        return False
    return verify_hashed_string(password, user.hashed_password)

def authenticate_refresh_token(db: Session, user_id: int, refresh_token: str) -> bool:
    """
    Authenticates a refresh token based on the user identifier and the provided refresh token.

        Parameters:
            db (Session): A database session.
            user_id (int): The user's identifier to check his refresh token.
            refresh_token (str): The provided refresh token to compare with user's refresh token.

        Returns:
            bool: Returns True if authentication succeeds, otherwise False.
    """
    user = get_user_by_id(db, user_id)
    if user is None:
        return False
    return verify_hashed_string(refresh_token, user.hashed_refresh_token)

def create_token(data: Dict, expires_delta: timedelta) -> str:
    """
    Creates a token (JWT) using JWT encoding.

        Parameters:
            data (Dict): A dictionary containing user-specific data to be included in the token payload.
            expires_delta (timedelta): Time after which the token expires.

        Returns:
            str: The created token (JWT).
    """
    to_encode = data.copy()
    expires = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, getenv("SECRET_KEY"), algorithm=getenv("ALGORITHM"))

def decode_token(token: str) -> Dict:
    """
    Decodes a token (JWT) using JWT decoding.

        Parameters:
            token (str): A token (JWT) to decode.

        Raises:
            InvalidCredentials: If the token (JWT) is incorrect.

        Returns:
            Dict: A dictionary that contains information from token (JWT).
    """
    try:
        return jwt.decode(token, getenv("SECRET_KEY"), algorithms=[getenv("ALGORITHM")])
    except JWTError:
        raise InvalidCredentials()
