from typing import Generator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.users.services import get_user_by_id
from backend.config import API_ENDPOINT
from backend.database.configuration import SessionLocal
from backend.users.schemas import UserOut
from backend.authentication.services import decode_token
from authentication.exceptions import InvalidCredentials


def get_db() -> Generator[SessionLocal, None, None]:
    """
    Database session to communicate with the database.

        Returns:
            Generator[SessionLocal, None, None]: A generator yielding a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_bearer = OAuth2PasswordBearer(tokenUrl=f"{API_ENDPOINT}/users/login")

def get_current_user(db: Session = Depends(get_db), access_token: str = Depends(oauth2_bearer)) -> UserOut:
    """
    Retrieves the currently authenticated user based on the provided access token (JWT).

        Parameters:
            db (Session): A database session.
            access_token (str): An access token (JWT) obtained from the authentication header.

        Raises:
            InvalidCredentials: If a user with an identifier from an access token is not found in the database.

        Returns:
            user (UserOut): Main information about the current user.
    """
    decoded_token = decode_token(access_token)
    user_id = decoded_token.get("sub")

    user = get_user_by_id(db, user_id)
    if user is None:
        raise InvalidCredentials()

    return user
