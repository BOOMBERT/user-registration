from pydantic import BaseModel, Field


class AccessToken(BaseModel):
    """
    Represents an access token (JWT) and its type.

         Parameters:
            access_token (str): The access token.
            token_type (str): The type of the access token.
    """
    access_token: str = Field(..., examples=["exampletoken"])
    token_type: str = Field(..., examples=["bearer"])


class RefreshToken(BaseModel):
    """
    Represents a refresh token (JWT) and its type.

        Parameters:
            refresh_token (str): The refresh token.
            token_type (str): The type of the refresh token.
    """
    refresh_token: str = Field(..., examples=["exampletoken"])
    token_type: str = Field(..., examples=["bearer"])


class Tokens(AccessToken, RefreshToken):
    """
    Represents a refresh token and access token and their types

        Parameters:
            access_token (str): The access token.
            refresh_token (str): The refresh token.
            token_type (str): The type of the tokens.
    """
    pass
