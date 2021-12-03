import secrets
import uuid
from typing import Optional

from starlette.requests import Request

from cphmr.db import DB
from cphmr.exceptions import ErrorCustomBruhher
from cphmr.scanner.exceptions.errors import ErrorBase
from cphmr.scanner.models.requests import AuthenticationRequest
from cphmr.scanner.models.responses import (
    AuthenticationResponse,
    AuthorizedStatusForResponse,
    NodeInfoForResponse,
    ResponseBase,
)
from cphmr.scanner.typesa import ActionTypes, ErrorTypes
from cphmr.typesa import APIKeysTypes


class AuthenticationRegistration:
    """
    Validates request parameters and authenticates the node.
    """

    @staticmethod
    def checkRequestParameters(request: Request,
                               body: AuthenticationRequest) -> bool:
        """
        Checks the request parameters.
        """
        authorizationHeader: Optional[str] = request.headers.get("X-API-Key")
        if not authorizationHeader:
            raise ErrorCustomBruhher(
                statusCode=400,
                response=ResponseBase(
                    action=ActionTypes.ERROR,
                    error=ErrorBase(
                        name=ErrorTypes.NO_RH_XAPK,
                        description="No X-API-Key header found.",
                    ),
                ),
            )
        actionType = getattr(
            ActionTypes,
            body.action.upper(),
            ActionTypes.ERROR,
        )
        if actionType != ActionTypes.AUTHENTICATE_REQUEST:
            raise ErrorCustomBruhher(
                statusCode=400,
                response=ResponseBase(
                    action=ActionTypes.ERROR,
                    error=ErrorBase(
                        name=ErrorTypes.UNK_ACT,
                        description="Action is either unknown or not supported.",
                    ),
                ),
            )
        return True

    @staticmethod
    def checkForValidKeys(request: Request, db: DB) -> bool:
        """
        Checks if the key is valid.
        """
        authorizationHeader: Optional[str] = request.headers.get("X-API-Key")
        if db.checkKey(authorizationHeader,
                       APIKeysTypes.SCANNER_NODE_REGISTRATION):
            return True
        raise ErrorCustomBruhher(
            statusCode=401,
            response=ResponseBase(
                action=ActionTypes.AUTHENTICATE_REJECT,
                error=ErrorBase(
                    name=ErrorTypes.F_K_NOF,
                    description="The key is not valid.",
                ),
            ),
        )

    @staticmethod
    def registerNode(request: Request, db: DB) -> ResponseBase:
        """
        Registers the node.
        """
        connectedIP: str = request.client.host
        nodeID: str = uuid.uuid4().__str__()
        nodeToken: str = secrets.token_hex(128).__str__()
        db.addScannerNode(nodeID=nodeID,
                          nodeToken=nodeToken,
                          connectedIP=connectedIP)
        return ResponseBase(
            action=ActionTypes.AUTHENTICATE_ACCEPT,
            result=AuthenticationResponse(
                authorization=AuthorizedStatusForResponse(succcess=True, ),
                nodeInfo=NodeInfoForResponse(nodeID=nodeID,
                                             nodeToken=nodeToken),
            ),
        )
