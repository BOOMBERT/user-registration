from fastapi import HTTPException, status


class EmailAlreadyRegistered(HTTPException):
    """
    Custom exception class for indicating that an email address is already registered.

        Attributes:
            STATUS_CODE (int): The HTTP status code for this exception, set to 409 Conflict.
            DETAIL (str): The detailed error message indicating that the email is already registered.
    """
    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = {
        "loc": ["body", "email"],
        "msg": "Email address is already registered"
    }

    def __init__(self):
        """
        Initialize the EmailAlreadyRegistered exception.
        """
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL)
