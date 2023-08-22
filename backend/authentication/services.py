from typing import Dict
from ..users.schemas import UserInDB
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import jwt
from os import getenv

from ..users.services import get_user_by_email
from .. utils.password_hashing import verify_password


def authenticate_user(db: Session, email: str, password: str) -> bool | UserInDB:
    """
    Authenticate a user based on their email and password.

        Parameters:
            db (Session): The database session.
            email (str): The email address of the user to be authenticated.
            password (str): The password provided by the user for authentication.

        Returns:
            bool | UserInDB:
                - Returns False if authentication fails.
                - Returns a UserInDB instance if authentication succeeds.
    """
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: Dict, expires_delta: timedelta) -> str:
    """
    Creates an access token using JWT encoding.

        Parameters:
            data (Dict): A dictionary containing user-specific data to be included in the access token payload.
            expires_delta (timedelta): A time duration indicating the validity period of the access token.

        Returns:
            str: The generated access token.
    """
    to_encode = data.copy()
    expires = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, getenv("SECRET_KEY"), algorithm=getenv("ALGORITHM"))
