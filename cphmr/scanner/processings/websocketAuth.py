from typing import Optional

from cphmr.db import DB
from cphmr.scanner.exceptions.errors import ErrorBase
from cphmr.scanner.models.responses import ResponseBase
from cphmr.scanner.typesa import ActionTypes, ErrorTypes


class WebSocketAuthentication:
    """
    Validates, accepts and authenticates a scanner node to a websocket.
    """

    @staticmethod
    def checkByNodeID(nodeID: str, nodeToken: str, db: DB) -> Optional[bool]:
        """
        Checks if the nodeID and nodeToken are valid, and the node is not\
        already connected.

        Returns 1 if the node is valid, -1 or -2 if not.
        """
        if db.checkScannerNodeToken(nodeID, nodeToken):
            if not (
                db.getScannerNodeParameter(
                    nodeID, "info.status.hasConnectedToSocket")
            ):
                return 1
            return -1
        return -2

    @staticmethod
    def getNegativeResponse(tokenReject: bool = True) -> ResponseBase:
        """
        Generates a response message with the authentication-related error.
        """
        return ResponseBase(
            action=ActionTypes.ERROR,
            error=ErrorBase(
                name=ErrorTypes.TOK_REJ if tokenReject else ErrorTypes.NODE_CON_AL,
                description="Node connection attempt failed due to invalid token."
                if tokenReject
                else "Node is already connected to a socket.",
            ),
        )

    @staticmethod
    def setNodeConnected(nodeID: str, db: DB, disconnect: bool = False) -> None:
        """
        Sets the node as connected to a socket.
        """
        db.updateScannerNode(
            nodeID, "info.status.hasConnectedToSocket", not (disconnect)
        )
