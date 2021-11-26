import secrets
import uuid
from typesa import ScanerMessageActionTypes


def generateNewToken() -> str:
    """Returns a string with a token (128 bits long)."""
    return str(secrets.token_hex(128))


def generateUUID() -> str:
    """Returns a UUID in form of string with dashes."""
    return str(uuid.uuid4())


def getActionTypeFromString(actionString: str) -> ScanerMessageActionTypes:
    """Returns the action type from a string."""
    return getattr(
        ScanerMessageActionTypes,
        actionString,
        ScanerMessageActionTypes.UNKNOWN_ACTION_RECEIVED
    )
