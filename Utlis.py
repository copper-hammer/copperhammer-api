import secrets

from Types import APIKeyTypes, ScannerSocketMessageTypes


def getScannerSocketMessageTypeAction(
        actionType: str) -> ScannerSocketMessageTypes:
    if actionType == "SET_NODE_ID":
        return ScannerSocketMessageTypes.SET_NODE_ID
    if actionType == "AUTHENTICATE_REQUEST":
        return ScannerSocketMessageTypes.AUTHENTICATE_REQUEST
    if actionType == "AUTHENTICATE_ACCEPT":
        return ScannerSocketMessageTypes.AUTHENTICATE_ACCEPT
    if actionType == "AUTHENTICATE_REJECT":
        return ScannerSocketMessageTypes.AUTHENTICATE_REJECT
    if actionType == "AUTHENTICATE_ERROR":
        return ScannerSocketMessageTypes.AUTHENTICATE_ERROR
    if actionType == "YAGOOD_NODE":
        return ScannerSocketMessageTypes.YAGOOD_NODE
    if actionType == "SEND_BATCH":
        return ScannerSocketMessageTypes.SEND_BATCH
    if actionType == "BATCH_ACCEPT_CONFIRM":
        return ScannerSocketMessageTypes.BATCH_ACCEPT_CONFIRM
    if actionType == "SUBMIT_RESULTS":
        return ScannerSocketMessageTypes.SUBMIT_RESULTS
    if actionType == "RESULTS_ACCEPT_CONFIRM":
        return ScannerSocketMessageTypes.RESULTS_ACCEPT_CONFIRM
    if actionType == "RESULTS_REJECT":
        return ScannerSocketMessageTypes.RESULTS_REJECT
    if actionType == "RESULTS_ERROR":
        return ScannerSocketMessageTypes.RESULTS_ERROR
    if actionType == "OVERALL_ERROR":
        return ScannerSocketMessageTypes.OVERALL_ERROR
    if actionType == "NODE_ERROR":
        return ScannerSocketMessageTypes.NODE_ERROR
    if actionType == "JSON_ERROR":
        return ScannerSocketMessageTypes.JSON_ERROR
    if actionType == "NOTENOUGHARGS_ERROR":
        return ScannerSocketMessageTypes.NOTENOUGHARGS_ERROR
    return ScannerSocketMessageTypes.UNKNOWN_ACTION_RECEIVED


def generateNewAPIKey() -> str:
    return str(secrets.token_hex(128))
