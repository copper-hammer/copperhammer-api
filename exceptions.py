class ErrorCustomBruhher(Exception):
    """
    Custom error exception for FastAPI.

    Args:
        action (str): The action type according to `typesa.ScanerMessageActionTypes`.
        detail (str): Description string of the error.
        statusCode (int): HTTP status code.
        isHTTP (bool): If True, the error is a HTTP error. (Currently unused, but might be used in the future, but for now it's always True, so it's not needed.)
    """

    def __init__(self,
                 action: str,
                 detail: str,
                 statusCode: int,
                 isHHTP: bool = True):
        """Initializes and stores actionType, detailed description and statusCode"""
        self.action = action
        self.detail = detail
        self.statusCode = statusCode
        self.isHTTP = isHHTP
