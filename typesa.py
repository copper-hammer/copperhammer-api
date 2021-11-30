from enum import Enum


class EnvironmentVariablesTypes(Enum):
    """
    Environment variables types (used to access the DB, the API, etc).
    """

    # Main
    MASTER_KEY = "MASTER_KEY"
    WEBSERVER_PORT = "WEBSERVER_PORT"
    # DB
    MONGODB_HOST = "MONGODB_HOST"
    MONGODB_PORT = "MONGODB_PORT"
    MONGODB_USERNAME = "MONGODB_USERNAME"
    MONGODB_PASSWORD = "MONGODB_PASSWORD"
    MONGODB_DB_NAME = "MONGODB_DB_NAME"
    MONGODB_AUTH_DB = "MONGODB_AUTH_DB"


class APIKeysTypes(Enum):
    """
    List of possible API key types
    (used to simplify the process of checking and storing).
    """

    SCANNER_NODE_REGISTRATION = "SCANNER_NODE_REGISTRATION"


class ScanerMessageActionTypes(Enum):
    """
    List of possible actions for the scanner message.
    """

    # Used in HTTP API
    AUTHENTICATE_REQUEST = "AUTHENTICATE_REQUEST"
    AUTHENTICATE_ACCEPT = "AUTHENTICATE_ACCEPT"
    AUTHENTICATE_REJECT = "AUTHENTICATE_REJECT"

    TOKEN_REJECT = "TOKEN_REJECT"

    YAGOOD_NODE = "YAGOOD_NODE"
    """
    Just a dummy `actionType` to check if connection's working.
    
    Can be used by both the server and a node.
    
    Example of expected message from `SCANNERNODE`:
    ```json
    {
        "action": "YAGOOD_NODE"
    }
    ```
    
    Example of expected message from `SERVER`:

    ```json
    {
        "action": "YAGOOD_NODE",
        "result": {
            "message": "Yep, I'm good!"
        },
        "error": {
            "fr": false,
            "msg": null
        }
    }
    ```
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
    In the current version and design, the server will send only one IP address at a time.
    
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
        },
        "error": {
            "fr": false,
            "msg": null
        }
    }
    ```
    """

    SEND_BATCH_REJECT = "SEND_BATCH_REJECT"
    """
    States to a node that the batch request was rejected due to its being either busy or due to an error. 
    This message shouldn't be sent in any circumstances, but it's here just in case.
    
    Can only be used by the server.
    
    Example of expected message from `SERVER`:
    ```json
    {
        "action": "SEND_BATCH_REJECT",
        "result": null,
        "error": {
            "fr": true,
            "msg": "SBRE_SNLOCK - The request to batch was rejected due to the node being busy."
        }
    }
    ```
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
    The node will then be removed from the list (actually, the property `status.isBusy`) of nodes that are currently scanning.
    
    Can only be used by the server.
    
    Example of expected message from `SERVER`:
    ```json
    {
        "action": "RESULTS_ACCEPT_CONFIRM",
        "result": {
            "message": "The results were accepted."
        },
        "error": {
            "fr": false,
            "msg": null
        }
    }
    ```
    """

    RESULTS_REJECT = "RESULTS_REJECT"
    """
    States to a node that the results submission request was rejected due to an error or wrong batchID. 
    This message shouldn't be sent in any circumstances, but it's here just in case.
    
    Can only be used by the server.
    
    Example of expected message from `SERVER`:
    ```json
    {
        "action": "RESULTS_REJECT",
        "result": null,
        "error": {
            "fr": true,
            "msg": "WR_BID - The batch ID is invalid."
        }
    }
    ```
    """

    OVERALL_ERROR = "OVERALL_ERROR"
    """
    States to a node that the request didn't succeed due to an unexpected error. 
    This message shouldn't be sent in any circumstances, but it's here just in case.
    
    Can only be used by the server.
    
    Example of expected message from `SERVER`:
    ```json
    {
        "action": "OVERALL_ERROR",
        "result": null,
        "error": {
            "fr": true,
            "msg": "N_ERROR - An error occurred."
        }
    }
    ```
    """

    MALFORMED_MESSAGE = "MALFORMED_MESSAGE"
    """
    States to a node that the request didn't succeed due to the message being malformed (for example, `JSONDecodeError`). 
    This message shouldn't be sent in any circumstances, but it's here just in case.
    
    Can only be used by the server.
    
    Example of expected message from `SERVER`:
    ```json
    {
        "action": "MALFORMED_MESSAGE",
        "result": null,
        "error": {
            "fr": true,
            "msg": "MALMJS - Received message is not a valid json."
        }
    }
    ```
    """

    NOTENOUGHARGS_ERROR = "NOTENOUGHARGS_ERROR"
    """
    States to a node that the request didn't succeed due to one or more fields missing in the message. 
    This message shouldn't be sent in any circumstances, but it's here just in case.
    
    Can only be used by the server.
    
    Example of expected message from `SERVER`:
    ```json
    {
        "action": "NOTENOUGHARGS_ERROR",
        "result": null,
        "error": {
            "fr": true,
            "msg": "NOEARE - Some fields are missing in the message."
        }
    }
    ```
    """

    UNKNOWN_ACTION_RECEIVED = "UNKNOWN_ACTION_RECEIVED"
    """
    States to a node that the request didn't succeed due to the action being unknown.
    This message shouldn't be sent in any circumstances, but it's here just in case.
    
    Can only be used by the server.
    
    Example of expected message from `SERVER`:
    ```json
    {
        "action": "UNKNOWN_ACTION_RECEIVED",
        "result": null,
        "error": {
            "fr": true,
            "msg": "UNACRE - Unknown action was received."
        }
    }
    ```
    """

    # TODO: Duplicate of `UNKNOWN_ACTION_RECEIVED` (see above)
    UNSUPPORTED_ACTION_RECEIVED = "UNSUPPORTED_ACTION_RECEIVED"
