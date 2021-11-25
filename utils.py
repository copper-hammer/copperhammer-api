import secrets
import uuid


def generateNewToken() -> str:
    """Returns a string with a token (128 bits long)."""
    return str(secrets.token_hex(128))


def generateUUID() -> str:
    """Returns a UUID in form of string with dashes."""
    return str(uuid.uuid4())
