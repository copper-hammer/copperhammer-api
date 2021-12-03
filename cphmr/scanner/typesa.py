from enum import Enum


class ActionTypes(Enum):
    """
    List of possible actions for the scanner message.
    """

    AUTHENTICATE_REQUEST = "AUTHENTICATE_REQUEST"
    AUTHENTICATE_ACCEPT = "AUTHENTICATE_ACCEPT"
    AUTHENTICATE_REJECT = "AUTHENTICATE_REJECT"

    YAGOOD_NODE = "YAGOOD_NODE"
    """
    Just a dummy `actionType` to check if connection's working.

    Can only be used by a node.
    """

    YAGOOD_SERVER = "YAGOOD_SERVER"
    """
    Simirally to `YAGOOD_NODE`, just a dummy `actionType` to check\
    if connection's working.

    Can only be used by the server.
    """

    REQUEST_BATCH = "REQUEST_BATCH"
    """
    States that the node is ready to receive a batch of IP addresses.

    Can only be used by a node.

    Example of expected message from `SCANNERNODE`:
    ```json
    {
        "action": "REQUEST_BATCH",
        "result": {
            "workers": 8
        }
    }
    ```
    """

    SEND_BATCH = "SEND_BATCH"
    """
    Sends a batch of IP addresses to a node as a response to `REQUEST_BATCH`.
    In the current version and design, the server will send only one IP\
    address at a time.

    Can only be used by the server.

    Example of expected message from `SERVER`:
    ```json
    {
        "action": "SEND_BATCH",
        "result": {
            "batch": [
                {
                    "serverIP": "127.0.0.1",
                    "portRange": {
                        "start": 3210,
                        "end": 28696
                    },
                    "batchID": "03dc0b97-b468-4190-a0b5-bba49fc323dd",
                }
            ]
        }
    }
    ```
    """

    SEND_BATCH_REJECT = "SEND_BATCH_REJECT"
    """
    States to a node that the batch request was rejected due to its being either\
    busy or due to an error.
    This message shouldn't be sent in any circumstances, but it's here just in case.

    Can only be used by the server.

    The `error` field is required with this type.
    """

    BATCH_ACCEPT_CONFIRM = "BATCH_ACCEPT_CONFIRM"
    """
    States that the node has received the batch and is ready to start scanning.

    Can only be used by a node.

    Example of expected message from `SCANNERNODE`:
    ```json
    {
        "action": "BATCH_ACCEPT_CONFIRM",
        "result": {
            "batchInfo": {
                "batchID": "03dc0b97-b468-4190-a0b5-bba49fc323dd",
                "serverIP": "127.0.0.1"
            }
        }
    }
    ```
    """

    SUBMIT_RESULTS = "SUBMIT_RESULTS"
    """
    States that the node has finished the scanning and is submitting the results.

    Can only be used by a node.

    Example of expected message from `SCANNERNODE`:
    ```json
    {
        "action": "SUBMIT_RESULTS",
        "result": {
            "batchID": "03dc0b97-b468-4190-a0b5-bba49fc323dd",
            "results": [
                {
                    "host": "127.0.0.1",
                    "port": 25565,
                    "title": "lttstore.com",
                    "version": {
                        "name": "1.7.10",
                        "protocol": 5,
                        "is_modded": true,
                        "mods": [
                            "Forge@10.13.4.1614"
                        ]
                    },
                    "players": {
                        "online": 1,
                        "max": 1337,
                        "sample": [
                            {
                                "uuid": "a728ef5b-3502-455a-aa14-03f99ece56a5",
                                "name": "Jopa26"
                            }
                        ]
                    }
                }
            ],
            "stats": {
                "duration": 10.454
            }
        }
    }
    ```
    """

    RESULTS_ACCEPT_CONFIRM = "RESULTS_ACCEPT_CONFIRM"
    """
    States to a node that the results were accepted.
    The node will then be removed from the list (actually, the property\
    `status.isBusy`) of nodes that are currently scanning.

    Can only be used by the server.

    Example of expected message from `SERVER`:
    ```json
    {
        "action": "RESULTS_ACCEPT_CONFIRM",
        "result": {
            "message": "The results were accepted."
        }
    }
    ```
    """

    RESULTS_REJECT = "RESULTS_REJECT"
    """
    States to a node that the results submission request was rejected\
    due to an error or wrong batchID.
    This message shouldn't be sent in any circumstances, but it's here just in case.

    Can only be used by the server.

    The `error` field is required with this type.
    """

    ERROR = "ERROR"
    """
    States that the request didn't succeed due to an error.

    Can only be used by both a node and the server.

    The `error` field is required with this type.
    """


class ErrorTypes(Enum):
    """
    Enum of possible error types.
    """

    UNK_ER = "UNK_ER"
    """
    Unknown error.
    """

    WR_BAID = "WR_BAID"
    """
    The batch ID is invalid.
    """

    SN_BR_LOCK = "SN_BR_LOCK"
    """
    The request to batch was rejected due to the node being busy.
    """

    MAL_MSG = "MAL_MSG"
    """
    Received message is not a valid json.
    """

    NO_R_F = "NO_R_F"
    """
    Some fields are missing in the message.
    """

    UNK_ACT = "UNK_ACT"
    """
    Unknown action was received.
    """

    REQ_VAL_ER = "REQ_VAL_ER"
    """
    Request validation error.
    """

    F_K_NOF = "F_K_NOF"
    """
    No such API key.
    """

    TOK_REJ = "TOK_REJ"
    """
    Token was rejected.
    """

    NODE_CON_AL = "NODE_CON_AL"
    """
    Node is already connected.
    """

    NO_RH_XAPK = "NO_RH_XAPK"
    """
    X-API-Key header is missing.
    """
