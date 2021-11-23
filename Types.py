from enum import Enum


class APIKeyTypes(Enum):

    SCANNER = "API_SCANNER_KEY"


class ScannerSocketMessageTypes(Enum):

    SET_NODE_ID = "SET_NODE_ID"
    AUTHENTICATE_REQUEST = "AUTHENTICATE_REQUEST"
    AUTHENTICATE_ACCEPT = "AUTHENTICATE_ACCEPT"
    AUTHENTICATE_REJECT = "AUTHENTICATE_REJECT"
    AUTHENTICATE_ERROR = "AUTHENTICATE_ERROR"
    YAGOOD_NODE = "YAGOOD_NODE"
    SEND_BATCH = "SEND_BATCH"
    BATCH_ACCEPT_CONFIRM = "BATCH_ACCEPT_CONFIRM"
    SUBMIT_RESULTS = "SUBMIT_RESULTS"
    RESULTS_ACCEPT_CONFIRM = "RESULTS_ACCEPT_CONFIRM"
    RESULTS_REJECT = "RESULTS_REJECT"
    RESULTS_ERROR = "RESULTS_ERROR"
    OVERALL_ERROR = "OVERALL_ERROR"
    NODE_ERROR = "NODE_ERROR"
    JSON_ERROR = "JSON_ERROR"
    NOTENOUGHARGS_ERROR = "NOTENOUGHARGS_ERROR"
    UNKNOWN_ACTION_RECEIVED = "UNKNOWN_ACTION_RECEIVED"
