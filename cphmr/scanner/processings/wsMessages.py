import json
from json.decoder import JSONDecodeError
from unittest import result
from pydantic.error_wrappers import ValidationError

from starlette.websockets import WebSocket

from cphmr.db import DB
from cphmr.scanner.models.requests import WebSocketMessageRequest, YagoodNodeRequest
from cphmr.scanner.typesa import ActionTypes


class MessageProcessings:
    """
    Websocket message processing for a scanner node.

    The parent initializes the objects and calls processMessage.
    """

    def __init__(self, websocket: WebSocket, db: DB) -> None:
        """
        Initialize the websocket message processing.
        """
        self.__db = db  # skipcq: PTC-W0037
        self.__websocket = websocket  # skipcq: PTC-W0037

    def processMessage(self, messageData: str) -> None:  # skipcq: PYL-R0201
        """
        Process a message from the websocket.

        As a result should send a response to the websocket.
        """
        try:
            data = json.loads(messageData)
            model = WebSocketMessageRequest(**data)
            print(model.dict())
        except JSONDecodeError:
            print("Invalid JSON")
        except KeyError:
            print("Invalid model")
        except ValidationError:
            print("Invalid model")
