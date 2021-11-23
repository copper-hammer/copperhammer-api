import json

import tornado.websocket

from DB import DB
from Processings.ScannerProcessing import ScannerProcessing
from Types import ScannerSocketMessageTypes
from Utlis import getScannerSocketMessageTypeAction


class ScannerSocket(tornado.websocket.WebSocketHandler):

    _is_busy = False
    # _authenticated = False

    @property
    def isBusy(self) -> bool:
        return self._is_busy

    @isBusy.setter
    def isBusy(self, newValue: bool) -> None:
        self._is_busy = newValue

    @isBusy.getter
    def isBusy(self) -> bool:
        return self._is_busy

    def initialize(self, db: DB):
        self.__DB = db

    def open(self, *args, **kwargs):
        self.set_nodelay(True)
        ScannerProcessing.add_lws(self)

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
            # TODO: message processing - should the action switching done here or in the processing?
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
        pass

    def send_message(self, message):
        self.write_message(message)
