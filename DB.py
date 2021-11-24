from typing import Union

import pymongo

from Types import APIKeyTypes


class DB:
    """Main way of commnuication with MongoDB. Handles everything related to storing state, keys, etc"""

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        authSource: str = "admin",
        authMech: str = "SCRAM-SHA-256",
    ) -> None:
        client = pymongo.MongoClient(
            host=host,
            port=port,
            username=username,
            password=password,
            authSource=authSource,
            authMechanism=authMech,
        )
        self._clkap = client["cprhmr"]["apikeys"]
        self._clsnd = client["cprhmr"]["scanernodes"]
        self._clsrv = client["cprhmr"]["servers"]
        self._clresu = client["cprhmr"]["results"]

    def addApiKey(self, apiKey: str, typeKey: APIKeyTypes) -> None:
        mapping = {"key": apiKey, "type": typeKey.value}
        self._clkap.insert_one(mapping)

    def checkApiKey(self, apiKey: str, typeKey: APIKeyTypes) -> bool:
        return self._clkap.find_one({
            "key": apiKey,
            "type": typeKey.value
        }) is not None

    def addScannerNode(self, scannerNodeID: str, ipStr: str) -> None:
        mapping = {
            "uuid": scannerNodeID,
            "info": {
                "request_from_ip": ipStr,
                "stats": {
                    "batches_sent": 0,
                    "batches_processed": 0
                },
            },
            "status": {
                "is_busy": False,
                "authenticated": False,
                "currently_processing": None,
            },
        }
        self._clsnd.insert_one(mapping)

    def updateScannerNode(self, scanneNodeID: str, updateParameter: str,
                          newValue: Union[str, None, int]) -> None:
        self._clsnd.update_one({"uuid": scanneNodeID},
                               {"$set": {
                                   updateParameter: newValue
                               }})

    def removeScannerNode(self, scannerNodeID: str) -> None:
        self._clsnd.delete_one({"uuid": scannerNodeID})
