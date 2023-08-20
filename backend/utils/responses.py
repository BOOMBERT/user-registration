from typing import Dict


def build_example_response(detail: str) -> Dict:
    """
    Build an example response for API documentation.

        Parameters:
            detail (str): The detail message to be included in the example response.

        Returns:
            Dict: An example response dictionary suitable for API documentation.
    """
    return {
        "content": {
            "application/json": {
                "example": {
                    "detail": detail
                }
            }
        }
    }
