from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .exceptions import IncorrectEmailOrPassword
from ..utils.responses import build_example_response
from datetime import timedelta
from os import getenv

from ..users.schemas import UserIn
from .schemas import Token
from .services import authenticate_user, create_access_token
from ..dependencies import get_db


router = APIRouter(
    prefix="/login",
    tags=["login"]
)

@router.post(
    "/",
    summary="User login and access token creation",
    description=
    """
    <h1>Authenticate the user and create an access token from the provided information:</h1>
    
    email: User's registered email address.
    password: User's valid password.
    """,
    response_model=Token,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully created access token for authenticated user"
        },
        IncorrectEmailOrPassword.STATUS_CODE: {
            "description": "Incorrect email address or password",
            **build_example_response(
                IncorrectEmailOrPassword.DETAIL,
                IncorrectEmailOrPassword.HEADERS
            )
        }
    },
    response_description="Successfully created access token for authenticated user",
    status_code=status.HTTP_200_OK
)
async def login_for_access_token(form_data: UserIn, db: Session = Depends(get_db)):
    """
    Authenticates users and creates an access token.

        Parameters:
            form_data (UserIn): User input data containing email and password for authentication.
            db (Session): Database session. Defaults to Depends(get_db).

        Raises:
            IncorrectEmailOrPassword: If the user with entered email and password doesn't exist.

        Returns:
            Token: A dictionary containing the created access token and its type.
    """
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise IncorrectEmailOrPassword()

    access_token_expires = timedelta(minutes=float(getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
