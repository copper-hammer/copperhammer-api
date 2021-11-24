import secrets
import uuid

from Types import ScannerSocketMessageTypes


def getScannerSocketMessageTypeAction(
        actionType: str) -> ScannerSocketMessageTypes:
    return getattr(
        ScannerSocketMessageTypes,
        actionType,
        ScannerSocketMessageTypes.UNKNOWN_ACTION_RECEIVED,
    )


def generateNewAPIKey() -> str:
    return str(secrets.token_hex(128))


def generateUUID() -> str:
    return str(uuid.uuid4())
