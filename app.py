import json
from json.decoder import JSONDecodeError
from typing import Union

import starlette.websockets
from fastapi import FastAPI, Request, WebSocket
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from config import Config, checkEnvironment
from db import DB
from exceptions import ErrorCustomBruhher
from models import ScannerNodeRegistration
from processings import ScannerNodeProcessing
from typesa import APIKeysTypes, ScanerMessageActionTypes
from utils import generateNewToken, generateUUID, getActionTypeFromString

checkEnvironment()

db = DB(Config.getMongoDBURI(), Config.getMongoDBName())

app = FastAPI(debug=True,
              title="Copperhammer API",
              description="API for the CopperHammer")


@app.exception_handler(ErrorCustomBruhher)
def custom_error_bruhher(request: Request, exc: ErrorCustomBruhher):
    """Handles the response for the Custom error."""
    return JSONResponse(
        status_code=exc.statusCode,
        content={
            "action": exc.action,
            "result": None,
            "error": {
                "fr": True,
                "msg": exc.detail
            },
        },
    )


@app.exception_handler(RequestValidationError)
def validation_error_custom(request: Request, exc: RequestValidationError):
    """Handles the response for the Validation error."""
    return JSONResponse(
        status_code=400,
        content={
            "action": "REQUEST_VALIDATION_ERROR",
            "result": None,
            "error": {
                "fr":
                True,
                "msg":
                "RVER - Not enough arguments or the structure were encountered in the body",
            },
        },
    )


@app.get("/")
def main_root():
    """Handles the response for the root"""
    mapping = {"bruh": True}
    return mapping


@app.post("/scanner/node_register", status_code=200)
def post_scanner_node_register8(request: Request,
                                body: ScannerNodeRegistration):
    """Handles the regustration of a new node."""
    authorizationHeader: Union[str, None] = request.headers.get("X-API-Key")
    connectedIP: str = request.client.host
    if authorizationHeader is None:
        raise ErrorCustomBruhher(
            action=ScanerMessageActionTypes.AUTHENTICATE_REJECT.value,
            statusCode=401,
            detail="NO_AUH - No authorization header",
        )
    if body.action != ScanerMessageActionTypes.AUTHENTICATE_REQUEST.value:
        raise ErrorCustomBruhher(
            action=ScanerMessageActionTypes.UNSUPPORTED_ACTION_RECEIVED.value,
            statusCode=400,
            detail="IN_ACR - Unsupported action received",
        )
    if db.checkKey(authorizationHeader,
                   APIKeysTypes.SCANNER_NODE_REGISTRATION):
        nodeID = generateUUID()
        nodeToken = generateNewToken()
        db.addScannerNode(nodeID=nodeID,
                          nodeToken=nodeToken,
                          connectedIP=connectedIP)
        mapping = {
            "action": ScanerMessageActionTypes.AUTHENTICATE_ACCEPT.value,
            "result": {
                "authorization": {
                    "success": True
                },
                "nodeInfo": {
                    "nodeID": nodeID,
                    "nodeToken": nodeToken
                },
            },
            "error": {
                "fr": False,
                "msg": None
            },
        }
        return mapping
    raise ErrorCustomBruhher(
        action=ScanerMessageActionTypes.AUTHENTICATE_REJECT.value,
        statusCode=401,
        detail="F_K_NOF - No such authorization key with the corresponding type found",
    )


@app.websocket("/scanner/node/{nodeID}")
async def websocket_endpoint_scanner_node(websocket: WebSocket, nodeID: str,
                                          token: str):
    """Handles websocket messaging for the scanner node."""
    try:
        if db.checkScannerNodeToken(
                nodeID=nodeID, nodeToken=token
        ) and not (db.getScannerNodeParameter(
                nodeID=nodeID,
                parameterString="info.status.hasConnectedToSocket") is True):
            try:
                await websocket.accept()
                SCNOPR = ScannerNodeProcessing(db,
                                               nodeID=nodeID,
                                               websocket=websocket)
                while True:
                    data = await websocket.receive_text()
                    try:
                        data = json.loads(data)
                        await SCNOPR.processMessage(
                            message=data,
                            actionType=getActionTypeFromString(data["action"]),
                        )
                    except JSONDecodeError:
                        mapping = {
                            "action":
                            ScanerMessageActionTypes.MALFORMED_MESSAGE.value,
                            "result": None,
                            "error": {
                                "fr":
                                True,
                                "msg":
                                "MALMJS - Received message is not a valid json",
                            },
                        }
                        await websocket.send_json(mapping)
                        await SCNOPR.gracefullyDisconnect(1002)
                    except KeyError:
                        mapping = {
                            "action":
                            ScanerMessageActionTypes.NOTENOUGHARGS_ERROR.value,
                            "result":
                            None,
                            "error": {
                                "fr":
                                True,
                                "msg":
                                "NOEARE - In the received json some field were not found",
                            },
                        }
                        await websocket.send_json(mapping)
                        await SCNOPR.gracefullyDisconnect(1002)
            except starlette.websockets.WebSocketDisconnect:
                await SCNOPR.gracefullyDisconnect(1000,
                                                  clientSideDisconnect=True)
        mapping = {
            "action": ScanerMessageActionTypes.TOKEN_REJECT.value,
            "result": None,
            "error": {
                "fr":
                True,
                "msg":
                "TOREJ - Token was either rejected, does not belong to this node or this node is already connected",
            },
        }
        await websocket.accept()
        await websocket.send_json(mapping)
        await websocket.close(code=1008)
    except starlette.websockets.WebSocketDisconnect:
        pass
    # TODO: Need to understand why sometimes `AssertionError` can be raised by `starlette` when closing websocket (server-side).
    except AssertionError:
        pass
