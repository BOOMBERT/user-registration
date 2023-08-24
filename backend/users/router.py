from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import timedelta
from os import getenv
from fastapi.security import OAuth2PasswordRequestForm

from backend.users import services
from backend.users.exceptions import EmailAlreadyRegistered
from .schemas import UserIn, UserOut, UserInDB
from ..dependencies import get_db, get_current_user
from ..utils import responses
from ..authentication.schemas import Token
from ..authentication.exceptions import IncorrectEmailOrPassword
from ..authentication.services import authenticate_user, create_access_token


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
    password: User's password that must meet the following criteria:
        - eight characters,
        - one uppercase letter,
        - one lowercase letter,
        - one number
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
    Creates a new user and adds it to the database if the email is not already registered.

        Parameters:
            user (UserIn): Input data for creating the user.
            db (Session): Database session. Defaults to Depends(get_db).

        Raises:
            EmailAlreadyRegistered: If the email is already registered.

        Returns:
            UserOut: Information about the created user.
    """
    db_user = services.get_user_by_email(db, user.email)
    if db_user:
        raise EmailAlreadyRegistered()

    return services.create_user(db, user)


@router.post(
    "/login",
    summary="Login the user and create an access token",
    description="""
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
            **responses.build_example_response(
                IncorrectEmailOrPassword.DETAIL,
                IncorrectEmailOrPassword.HEADERS
            )
        }
    },
    response_description="Successfully created access token for authenticated user",
    status_code=status.HTTP_200_OK
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise IncorrectEmailOrPassword()

    access_token_expires = timedelta(minutes=float(getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/me",
    summary="Get the current user",
    description="""
    <h1>Get the currently authenticated user.</h1>
    """,
    response_model=UserOut,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully obtained an authenticated user"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not authenticated user",
            **responses.build_example_response("Not authenticated")
        }
    },
    response_description="Successfully obtained an authenticated user",
    status_code=status.HTTP_200_OK
)
async def get_me(user: UserInDB = Depends(get_current_user)):
    """
    Get the currently authenticated user.
    In addition, this is an example route to show how to authenticate the route by user authentication.

        Parameters:
            user (UserInDB): The Information of the current user from database. Defaults to Depends(get_current_user).

        Returns:
            user (UserOut): Information about the current user.
    """
    return user
