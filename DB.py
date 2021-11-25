import pymongo

from typesa import APIKeysTypes


class DB:
    """Manages communication with the MongoDB."""

    def __init__(self, mogusURI: str, dbName: str) -> None:
        """Initializes the DB object."""
        client = pymongo.MongoClient(mogusURI)
        self.__apikeys = client[dbName]["apikeys"]
        self.__scannernodes = client[dbName]["scannernodes"]

    def checkKey(self, apiKey: str, keyType: APIKeysTypes) -> bool:
        """
        Checks if the API key is in the database.

        Returns True if the key is in the database, False otherwise.
        """
        return (self.__apikeys.find_one({
            "key": apiKey,
            "type": keyType.value
        }) is not None)

    def addScannerNode(self, nodeID: str, nodeToken: str,
                       connectedIP: str) -> None:
        """
        Adds a new scanner node to the database.

        Node is a dictionary with the following structure:
        ```json
        {
            "nodeID": "UUID",
            "token": "TOKEN",
            "info": {
                "connectedFrom": "IP",
                "status": {
                    "hasConnectedToSocket": false,
                    "isBusy": false,
                },
                "stats": {
                    "batchesSent": 0,
                    "batchesReceived": 0,
                    "serversFound": 0
                }
            }
        }
        ```
        """
        mapping = {
            "nodeID": nodeID,
            "token": nodeToken,
            "info": {
                "connectedFrom": connectedIP,
                "status": {
                    "hasConnectedToSocket": False,
                    "isBusy": False,
                },
                "stats": {
                    "batchesSent": 0,
                    "batchesReceived": 0,
                    "serversFound": 0
                },
            },
        }
        self.__scannernodes.insert_one(mapping)

    def checkScannerNodeToken(self, nodeID: str, nodeToken: str) -> bool:
        """
        Checks if the node token is in the database.

        Returns True if the token is in the database, False otherwise.
        """
        return (self.__scannernodes.find_one({
            "nodeID": nodeID,
            "token": nodeToken
        }) is not None)
