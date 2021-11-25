class ErrorCustomBruhher(Exception):
    """Custom error exception for FastAPI."""

    def __init__(self, action: str, detail: str, statusCode: int):
        """Initializes and stores actionType, detailed description and statusCode"""
        self.action = action
        self.detail = detail
        self.statusCode = statusCode
