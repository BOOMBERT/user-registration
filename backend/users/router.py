from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from os import getenv

from backend.users import services
from backend.users.exceptions import EmailAlreadyRegistered
from .schemas import UserIn, UserOut
from ..dependencies import get_db, get_current_user
from ..utils import responses
from ..authentication.schemas import Tokens, AccessToken
from ..authentication.exceptions import IncorrectEmailOrPassword, InvalidCredentials
from ..authentication.services import authenticate_user, create_token, decode_token, authenticate_refresh_token


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post(
    "/register",
    summary="Register the user",
    description="""
    <h1>Creates a new user with the provided information:</h1>
    
    email: User's unregistered email address.
    password: User's password, which must include at least:
        - eight characters,
        - one uppercase character,
        - one lowercase character,
        - one digit
        In addition the password can't include more than 256 characters.
    """,
    response_model=UserOut,
    responses={
        status.HTTP_201_CREATED: {
            "description": "User created successfully",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Invalid email address or password",
        },
        EmailAlreadyRegistered.STATUS_CODE: {
            "description": "Already registered email address",
            **responses.build_example_response(EmailAlreadyRegistered.DETAIL)
        },
    },
    response_description="User created successfully",
    status_code=status.HTTP_201_CREATED
)
async def create_user(user: UserIn, db: Session = Depends(get_db)):
    """
    Creates a new user and adds it to the database if the email is not already registered and the password is strong.

        Parameters:
            user (UserIn): Input data to create a user (email and password).
            db (Session): A database session. Defaults to Depends(get_db).

        Raises:
            EmailAlreadyRegistered: If the email is already registered.

        Returns:
            UserOut: Main information about the created user.
    """
    db_user = services.get_user_by_email(db, user.email)
    if db_user:
        raise EmailAlreadyRegistered()

    return services.create_user(db, user)


@router.post(
    "/login",
    summary="Login the user",
    description="""
    <h1>Authenticates a user and creates an access token and a refresh token using the information provided:</h1>

    email: User's registered email address.
    password: User's valid password.
    """,
    response_model=Tokens,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully created an access token, a refresh token and authenticated the user"
        },
        IncorrectEmailOrPassword.STATUS_CODE: {
            "description": "Incorrect email address or password",
            **responses.build_example_response(
                IncorrectEmailOrPassword.DETAIL,
                IncorrectEmailOrPassword.HEADERS
            )
        }
    },
    response_description="Successfully created an access token, a refresh token and authenticated the user",
    status_code=status.HTTP_200_OK
)
async def login_for_tokens(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticates the user and creates an access token and a refresh token.

        Parameters:
            form_data (UserIn): User input data containing email and password for authentication.
            db (Session): A database session. Defaults to Depends(get_db).

        Raises:
            IncorrectEmailOrPassword: If the user with entered email and password does not exist.

        Returns:
            Tokens: A dictionary containing the created refresh token, access token and its type.
    """
    if not authenticate_user(db, email=form_data.username, password=form_data.password):
        raise IncorrectEmailOrPassword()

    user = services.get_user_by_email(db, email=form_data.username)

    access_token_expires = timedelta(minutes=float(getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(minutes=float(getenv("REFRESH_TOKEN_EXPIRE_MINUTES")))
    refresh_token = create_token(
        data={"sub": str(user.id)}, expires_delta=refresh_token_expires
    )
    services.hash_and_save_refresh_token_in_db(db, user.id, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get(
    "/refresh",
    summary="Refresh the access token",
    description="""
    <h1>Refreshes the access token from the provided information:</h1>
    
    refresh_token: The correct refresh token.
    """,
    response_model=AccessToken,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully refreshed access token"
        },
        InvalidCredentials.STATUS_CODE: {
            "description": "Invalid credentials",
            **responses.build_example_response(
                InvalidCredentials.DETAIL,
                InvalidCredentials.HEADERS
            )
        }
    },
    response_description="Successfully refreshed access token",
    status_code=status.HTTP_200_OK
)
async def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    Based on the refresh token, it creates an access token if the refresh token is correct.

        Parameters:
            refresh_token (str): A refresh token. Defaults to Depends(oauth2_bearer).
            db (Session): A database session. Defaults to Depends(get_db).

        Raises:
            InvalidCredentials: If the refresh token is incorrect.

        Returns:
            AccessToken: An access token and its type.
    """
    decoded_refresh_token = decode_token(refresh_token)
    user_id = decoded_refresh_token.get("sub")

    if authenticate_refresh_token(db, user_id, refresh_token):
        access_token_expires = timedelta(minutes=float(getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
        new_access_token = create_token(
            data={"sub": user_id}, expires_delta=access_token_expires
        )

        return {"access_token": new_access_token, "token_type": "bearer"}

    raise InvalidCredentials()


@router.get(
    "/me",
    summary="Get the current user",
    description="""
    <h1>Gets the currently authenticated user.</h1>
    """,
    response_model=UserOut,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully obtained an authenticated user"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not authenticated user",
            **responses.build_example_response(
                "Not authenticated"
            )
        }
    },
    response_description="Successfully obtained an authenticated user",
    status_code=status.HTTP_200_OK
)
async def get_me(user: UserOut = Depends(get_current_user)):
    """
    Gets the currently authenticated user.

        Parameters:
            user (UserOut): Main information about the current user. Defaults to Depends(get_current_user).

        Returns:
            user (UserOut): Main information about the current user.
    """
    return user
