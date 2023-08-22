from typing import Dict


def build_example_response(detail: str, headers: Dict = None) -> Dict:
    """
    Build an example response for API documentation.

        Parameters:
            detail (str): The detail message to be included in the example response.
            headers (Dict, optional): A dictionary of custom headers to be included in the example response.

        Returns:
            example_response (Dict): An example response dictionary suitable for API documentation.
    """
    example_response = {
        "content": {
            "application/json": {
                "example": {
                    "detail": detail
                }
            }
        }
    }

    if headers:
        example_response["content"]["application/json"].update({"headers": headers})

    return example_response
