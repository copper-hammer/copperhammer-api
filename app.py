from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

# ? Holy sheez, these dependencies are so much fun to manage!
from cphmr.config import Config, checkEnvironment
from cphmr.db import DB
from cphmr.exceptions import ErrorCustomBruhher
from cphmr.models.response import MainResponseBase
from cphmr.scanner.exceptions.errors import ErrorBase as ScannerErrorBase
from cphmr.scanner.models.requests import (
    AuthenticationRequest as ScannedAuthenticationRequest,
)
from cphmr.scanner.models.responses import ResponseBase as ScannerResponseBase
from cphmr.scanner.processings.authRegister import (
    AuthenticationRegistration as ScannerAuthenticationRegistration,
)
from cphmr.scanner.processings.websocketAuth import (
    WebSocketAuthentication as ScannerWebSocketAuthentication,
)
from cphmr.scanner.processings.wsMessages import (
    MessageProcessings as ScannerMessageProcessings,
)
from cphmr.scanner.typesa import ErrorTypes as ScannerErrorTypes

checkEnvironment()

db = DB(Config.getMongoDBURI(), Config.getMongoDBName())

app = FastAPI(
    debug=True, title="Copperhammer API", description="API for the CopperHammer"
)


@app.exception_handler(ErrorCustomBruhher)
def custom_error_bruhher(request: Request, exc: ErrorCustomBruhher) -> JSONResponse:
    """
    Handles the response for the Custom error.

    Returns JSONResponse with the error message.
    """
    return JSONResponse(status_code=exc.statusCode, content=exc.response.dict())


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(*_) -> JSONResponse:
    """
    Handles the response for the RequestValidationError.

    Returns JSONResponse with the error message.
    """
    return JSONResponse(
        status_code=400,
        content=MainResponseBase(
            error=ScannerErrorBase(
                name=ScannerErrorTypes.REQ_VAL_ER,
                description="Requset validation error.",
            )
        ).dict(),
    )


@app.post("/scanner/node_register", status_code=200, response_model=ScannerResponseBase)
def post_scanner_node_register(request: Request, body: ScannedAuthenticationRequest):
    """
    Handles the HTTP-based registration of a new node.
    Should be called by the scanner node on each launch.

    Should result in node being registered in the database and a token being\
    given to the node, otherwise rejected.
    """
    if ScannerAuthenticationRegistration.checkRequestParameters(
        request, body
    ) and ScannerAuthenticationRegistration.checkForValidKeys(request, db):
        return ScannerAuthenticationRegistration.registerNode(request, db)
    # ? Well, this return isn't necessar since everything will be caught in
    # ? exceptions... but I'm not sure if it's a good idea to do like that in
    # ? in the first place (but DeepSource says yes, soooo). I'll leave it
    # ? here for now.
    return None


# ? Is it even necessary to "unregister" a node? I don't think so.
# TODO: Scanner node unregistration `/scanner/node_unregister`


@app.websocket("/scanner/node/{nodeID}")
async def websocket_endpoint_scanner_node(
    websocket: WebSocket, nodeID: str, token: str
):
    """
    Handles websocket messaging for the scanner node.

    All messages are expected to be sent in JSON format following the structure:
    ```json
    {
        "action": "actionType",
        "result": {},
        "error": null
    }
    ```
    """
    await websocket.accept()
    authStatus = ScannerWebSocketAuthentication.checkByNodeID(
        nodeID=nodeID, nodeToken=token, db=db
    )
    # ? This is cringe, I think. But I don't know how to do it better.
    if authStatus == 1:
        # ScannerWebSocketAuthentication.setNodeConnected(nodeID=nodeID, db=db)
        SCNOPR = ScannerMessageProcessings(websocket=websocket, db=db)
        try:
            while True:
                SCNOPR.processMessage(await websocket.receive_text())
        except WebSocketDisconnect:
            ScannerWebSocketAuthentication.setNodeConnected(
                nodeID=nodeID, db=db, disconnect=True
            )
        except AssertionError:
            ScannerWebSocketAuthentication.setNodeConnected(
                nodeID=nodeID, db=db, disconnect=True
            )
    else:
        await websocket.send_json(
            ScannerWebSocketAuthentication.getNegativeResponse(
                False if authStatus == -1 else True  # skipcq: PYL-R1719
            ).dict()
        )
        await websocket.close(code=1008)
