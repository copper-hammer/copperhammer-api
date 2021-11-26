from typing import Union

from db import DB
from typesa import ScanerMessageActionTypes


class ScannerNodeProcessing:
    """
    Handles all the processing received from the node via wevsocket.
    """

    def __init__(self, db: DB, nodeID: str, websocket) -> None:
        """
        Initializes the class.

        Gets the nodeID and the websocket from the `websocket_endpoint_scanner_node`.
        """
        self.__DB = db
        self.__ws = websocket
        self._nodeID = nodeID
        self.currentlyProcessingBatchID: str = ""
        self.__DB.updateScannerNode(self._nodeID,
                                    "info.status.hasConnectedToSocket", True)

    async def gracefullyDisconnect(self,
                                   disconnectCode: int,
                                   clientSideDisconnect: bool = False) -> None:
        """
        Disconnects gracefully.
        """
        if not clientSideDisconnect:
            await self.__ws.close(code=disconnectCode)
        self.__DB.updateScannerNode(self._nodeID,
                                    "info.status.hasConnectedToSocket", False)
        if (self.__DB.getScannerNodeParameter(self._nodeID,
                                              "info.status.isBusy") is True):
            self.__DB.updateScannerNode(self._nodeID, "info.status.isBusy",
                                        False)
            self.__DB.unlockOneBatch(self.currentlyProcessingBatchID)

    async def processMessage(self, message: dict,
                             actionType: ScanerMessageActionTypes) -> None:
        """
        Processes the message received from the node.

        Returns the message to the node, otherwise returns None.
        """
        if actionType == ScanerMessageActionTypes.YAGOOD_NODE:
            answer = self.yagoodNode()
        elif actionType == ScanerMessageActionTypes.REQUEST_BATCH:
            if (self.__DB.getScannerNodeParameter(
                    self._nodeID, "info.status.isBusy") is False):
                self.__DB.updateScannerNode(self._nodeID, "info.status.isBusy",
                                            True)
                answer = self.requestBatch()
            else:
                answer = self.sendBatchReject()
        return await self.__ws.send_json(answer) if answer else None

    @staticmethod
    def yagoodNode() -> dict:
        """
        Answers to the node's YAGOOD message.

        Returns the message (`dict`) to the node.
        """
        return {
            "action": ScanerMessageActionTypes.YAGOOD_NODE.value,
            "result": {
                "message": "Yep, I'm good!"
            },
            "error": {
                "fr": False,
                "msg": None
            },
        }

    def requestBatch(self) -> dict:
        """
        Gets the node request to have a batch.

        Return the message (`dict`) to the node.
        """
        return {
            "action": ScanerMessageActionTypes.SEND_BATCH.value,
            "result": self.sendBatch(),
            "error": {
                "fr": False,
                "msg": None
            },
        }

    def sendBatch(self) -> Union[dict, None]:
        """
        Sends the batch to the node. Actually, it's preparing the batch.

        Returns the batch (`dict`), otherwise returns None if there is no batch.
        """
        batch = self.__DB.getOneBatchAndLockIt()
        print(batch)
        if batch:
            mapping = {
                "serverIP": batch["server"],
                "portRange": {
                    "start": 0,
                    "end": 65535
                },
                "batchID": batch["status"]["batchID"],
            }
            self.currentlyProcessingBatchID = batch["status"]["batchID"]
            return mapping
        return None

    @staticmethod
    def sendBatchReject() -> None:
        """
        Notifies the node that the batch request was rejected.
        """
        return {
            "action": ScanerMessageActionTypes.SEND_BATCH_REJECT.value,
            "result": None,
            "error": {
                "fr":
                True,
                "msg":
                "SBRE_SNLOCK - The request to batch was rejected due to the node being busy",
            },
        }

    def batchAcceptConfirm(self) -> None:
        """
        The node confirms the batch accept.
        """
        raise NotImplementedError()

    def submitResults(self) -> None:
        """
        Submits the results from the node.
        """
        raise NotImplementedError()

    def resultsAcceptConfirm(self) -> None:
        """
        Confirms to the node the results accept.
        """
        raise NotImplementedError()

    def resultsReject(self) -> None:
        """
        Rejects the results from the node.
        """
        raise NotImplementedError()

    def overallError(self) -> None:
        """
        Notifies the node about an error.
        """
        raise NotImplementedError()

    def malformedMessage(self) -> None:
        """
        Notifies the node about a malformed message.
        """
        raise NotImplementedError()

    def unknownAction(self) -> None:
        """
        Notifies the node about an unknown action.
        """
        raise NotImplementedError()
