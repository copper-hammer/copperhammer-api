import json
from typing import Union

import tornado.websocket

from DB import DB
from Processings.ScannerProcessing import ScannerProcessing
from Types import ScannerSocketMessageTypes
from Utlis import getScannerSocketMessageTypeAction


class ScannerSocket(tornado.websocket.WebSocketHandler):

    # Variables
    _is_busy: bool = False
    _node_id: Union[str, None] = None
    _authenticated: bool = False

    # is_busy is used to prevent the node from getting new tasks
    @property
    def isBusy(self) -> bool:
        return self._is_busy

    @isBusy.setter
    def isBusy(self, newValue: bool) -> None:
        self._is_busy = newValue
        self.__DB.updateScannerNode(self.nodeID, "status.is_busy", newValue)

    @isBusy.getter
    def isBusy(self) -> bool:
        return self._is_busy

    # Node ID property
    @property
    def nodeID(self) -> str:
        return self._node_id

    @nodeID.setter
    def nodeID(self, newValue: str) -> None:
        self._node_id = newValue

    @nodeID.getter
    def nodeID(self) -> str:
        return self._node_id

    # Authenticated propety
    @property
    def authenticated(self) -> bool:
        return self._authenticated

    @authenticated.setter
    def authenticated(self, newValue: bool) -> None:
        self._authenticated = newValue

    @authenticated.getter
    def authenticated(self) -> bool:
        return self._authenticated

    # Initializing
    def initialize(self, db: DB):
        self.__DB = db

    # Socket opener
    def open(self, *args, **kwargs):
        self.set_nodelay(True)
        ScannerProcessing.set_node_id(self)
        ScannerProcessing.add_lws(self, self.__DB)

    # Message switching
    def on_message(self, message: str):
        try:
            message = json.loads(message)
            actionType = getScannerSocketMessageTypeAction(message["action"])
            if actionType == ScannerSocketMessageTypes.UNKNOWN_ACTION_RECEIVED:
                mapping = {
                    "action":
                    ScannerSocketMessageTypes.UNKNOWN_ACTION_RECEIVED.value,
                    "result": None,
                    "error": {
                        "fr":
                        True,
                        "msg":
                        "UNKNOWNACTIONRECEIVED - The server received an unknown action",
                    },
                }
                self.write_message(str(mapping))
            if actionType == ScannerSocketMessageTypes.AUTHENTICATE_REQUEST:
                # {"action":"AUTHENTICATE_REQUEST","result":None,"error":{"fr":False,"msg":None},"node_id":"1",auth_key:"ligma"}
                ScannerProcessing.authenticate_request(self,
                                                       message["auth_key"],
                                                       self.__DB)
        except json.JSONDecodeError:
            mapping = {
                "action": ScannerSocketMessageTypes.JSON_ERROR.value,
                "result": None,
                "error": {
                    "fr":
                    True,
                    "msg":
                    "JSONDECODERROR - Couldn't process the JSON sent from the node",
                },
            }
            self.write_message(str(mapping))
            # It is expected that the node will send a proper JSON or will close a connection. Also, that prevents the node from getting new tasks.
        except KeyError:
            mapping = {
                "action": ScannerSocketMessageTypes.NOTENOUGHARGS_ERROR.value,
                "result": None,
                "error": {
                    "fr": True,
                    "msg": "KEYERROR - Certain required values were not found",
                },
            }
            self.write_message(str(mapping))
            self.close()
        except Exception as e:
            print(e)
            mapping = {
                "action": ScannerSocketMessageTypes.OVERALL_ERROR.value,
                "result": None,
                "error": {
                    "fr": True,
                    "msg": f"OVERALLERROR - {e}",
                },
            }
            self.write_message(str(mapping))
            self.close()

    def on_close(self):
        self.__DB.removeScannerNode(self.nodeID)

    def send_message(self, message):
        self.write_message(message)
