from cphmr.scanner.models.responses import ResponseBase as ScannerResponseBase


class ErrorCustomBruhher(Exception):
    """
    Custom error exception for FastAPI HTTP-endpoints.
    """

    def __init__(  # skipcq: PYL-W0231
            self,
            response: ScannerResponseBase,
            statusCode: int
    ) -> None:
        """
        Initialize the exception.

        Response is a ScannerResponseBase object, which contains the response.\
        statusCode is the HTTP-status code.
        """
        self.response = response
        self.statusCode = statusCode
