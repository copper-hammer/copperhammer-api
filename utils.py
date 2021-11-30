import secrets
import uuid

from typesa import ScanerMessageActionTypes


def generateNewToken() -> str:
    """
    Generates a new token with `Python`'s `secrets` module.

    Returns a string with a token (128 bits long).
    """
    return str(secrets.token_hex(128))


def generateUUID() -> str:
    """
    Generates a new UUID with `Python`'s `uuid` module.

    Returns a UUID in form of string with dashes.
    """
    return str(uuid.uuid4())


def getActionTypeFromString(actionString: str) -> ScanerMessageActionTypes:
    """
    Parses a string to a `ScanerMessageActionTypes` enum.

    Returns the action type from a string.
    """
    return getattr(
        ScanerMessageActionTypes,
        actionString,
        ScanerMessageActionTypes.UNKNOWN_ACTION_RECEIVED,
    )
