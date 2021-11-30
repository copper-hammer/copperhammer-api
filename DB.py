from typing import Union

import pymongo

from typesa import APIKeysTypes


class DB:
    """
    Manages communication with the MongoDB database.

    All methods are not static, they should be called from the main program.
    """

    def __init__(self, mogusURI: str, dbName: str) -> None:
        """
        Initializes the DB object from the given URI and DB name.

        Stores the collections in the corresponding objects.
        """
        client = pymongo.MongoClient(mogusURI)
        self.__apikeys = client[dbName]["apikeys"]
        self.__scannernodes = client[dbName]["scannernodes"]
        self.__queueservers = client[dbName]["queueservers"]

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
                    "workingOn": null,
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
                    "workingOn": None,
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

    def getScannerNodeParameter(
            self, nodeID: str,
            parameterString: str) -> Union[str, int, bool, None]:
        """
        Gets the scanner node with the given ID.

        It is expected that the node exists in the database.
        Returns the value of the parameter with the given name if it exists, None otherwise.
        """
        try:
            answbp = self.__scannernodes.find_one({"nodeID": nodeID})
            for value in parameterString.split("."):
                answbp = answbp[value]
            return answbp
        except KeyError:
            return None

    def updateScannerNode(self, nodeID: str, paramaterString: str,
                          newValue: Union[str, int, bool]) -> None:
        """
        Updates a scanner node in the database.

        It is expected that the node exists in the database.
        Updates the value of the parameter with the given name.
        """
        self.__scannernodes.update_one({"nodeID": nodeID},
                                       {"$set": {
                                           paramaterString: newValue
                                       }})

    def addBatchToQueue(self, batch: dict) -> None:
        """
        Adds a batch to the queue.

        The batch is a `dict` following the structure:
        ```json
        {
            "server": "80.249.178.190",
            "status": {
                "locked": false,
                "batchID": "3560ab0c-7925-4510-bef1-984479873963"
            }
        }
        ```
        """
        try:
            self.__queueservers.insert_one(batch)
        except pymongo.errors.DuplicateKeyError:
            pass

    def getOneBatchAndLockIt(self) -> Union[dict, None]:
        """
        Gets one batch from the database.

        Returns the batch as a dictionary if it exists and is not locked, None otherwise.
        """
        return self.__queueservers.find_one_and_update(
            {"status.locked": False}, {"$set": {
                "status.locked": True
            }})

    def unlockOneBatch(self, batchID: str) -> None:
        """
        Unlocks one batch.

        The batch is identified by its ID.
        """
        self.__queueservers.update_one({"status.batchID": batchID},
                                       {"$set": {
                                           "status.locked": False
                                       }})

    # TODO: add node session closing
