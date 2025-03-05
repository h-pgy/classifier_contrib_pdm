from requests.exceptions import HTTPError

class NoContentError(HTTPError):
    """Custom exception for 204 No Content responses."""
    def __init__(self, message="204 No Content: The server returned no data.", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.status_code = 204  # Add the status code as an attribute