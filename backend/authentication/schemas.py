from pydantic import BaseModel, Field


class Token(BaseModel):
    """
    Represents an authentication token with essential information.

        Parameters:
            access_token (str): The access token string representing the authentication.
            token_type (str): The type of the access token.
    """
    access_token: str = Field(..., examples=["exampletoken"])
    token_type: str = Field(..., examples=["bearer"])
