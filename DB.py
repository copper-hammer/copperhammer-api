import pymongo

from Types import APIKeyTypes


class DB:
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