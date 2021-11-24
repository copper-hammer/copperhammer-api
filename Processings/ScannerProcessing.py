from DB import DB
from Types import APIKeyTypes, ScannerSocketMessageTypes
from Utlis import generateUUID


class ScannerProcessing:
    """Handles functions of the scanner websocket"""

    __alws = []

    @classmethod
    def add_lws(cls, websocket, db: DB) -> None:
        cls.__alws.append(websocket)
        db.addScannerNode(websocket.nodeID, websocket.request.remote_ip)
        websocket.isBusy = False

    @classmethod
    def remove_nonworking_sockets(cls, db: DB) -> None:
        to_be_removed = set()
        for websocket in cls.__alws:
            if not websocket.ws_connection or not websocket.ws_connection.stream.socket:
                to_be_removed.add(websocket)
        for websocket in to_be_removed:
            db.removeScannerNode(websocket.nodeID)
            cls.__alws.remove(websocket)

    @classmethod
    def list_alwss(cls, db: DB) -> list:
        cls.remove_nonworking_sockets(db)
        for vsocket in cls.__alws:
            yield {
                "nodeID": vsocket.nodeID,
                "isBusy": vsocket.isBusy,
                "isAuthenticated": vsocket.authenticated,
                "socketObject": str(vsocket),
            }

    @classmethod
    def send_message(cls, message, db: DB) -> int:
        cls.remove_nonworking_sockets(db)
        for vsocket in cls.__alws:
            if not vsocket.isBusy:
                vsocket.isBusy = True
                vsocket.send_message(message)
                return 1
        return 0

    @classmethod
    def set_node_id(cls, websocket) -> None:
        websocket.nodeID = generateUUID()
        mapping = {
            "action": ScannerSocketMessageTypes.SET_NODE_ID.value,
            "result": {
                "node_id": websocket.nodeID
            },
            "error": {
                "fr": False,
                "msg": None,
            },
        }
        websocket.send_message(str(mapping))

    @classmethod
    def authenticate_request(cls, websocket, keyStr: str, db: DB) -> None:
        if db.checkApiKey(keyStr, APIKeyTypes.SCANNER):
            mapping = {
                "action": ScannerSocketMessageTypes.AUTHENTICATE_ACCEPT.value,
                "result": {
                    "authenticated:": {
                        "success": True
                    }
                },
                "error": {
                    "fr": False,
                    "msg": None,
                },
            }
            websocket.authenticated = True
            db.updateScannerNode(websocket.nodeID, "status.authenticated",
                                 True)
            websocket.send_message(str(mapping))
        else:
            mapping = {
                "action": ScannerSocketMessageTypes.AUTHENTICATE_REJECT.value,
                "result": {
                    "authenticated:": {
                        "success": False
                    }
                },
                "error": {
                    "fr": False,
                    "msg": None,
                },
            }
            websocket.send_message(str(mapping))
            cls.__alws.remove(websocket)
            db.removeScannerNode(websocket.nodeID)
            websocket.close()

    @classmethod
    def authenticate_accept(cls, websocket, message) -> None:
        raise NotImplementedError()

    @classmethod
    def authenticate_reject(cls, websocket, message) -> None:
        raise NotImplementedError()

    @classmethod
    def authenticate_error(cls, websocket, message) -> None:
        raise NotImplementedError()

    @classmethod
    def yagood_node(cls, websocket, message) -> None:
        raise NotImplementedError()

    @classmethod
    def send_batch(cls, websocket, message) -> None:
        raise NotImplementedError()

    @classmethod
    def batch_accept_confirm(cls, websocket, message) -> None:
        raise NotImplementedError()

    @classmethod
    def submit_results(cls, websocket, message) -> None:
        raise NotImplementedError()

    @classmethod
    def results_accept_confirm(cls, websocket, message) -> None:
        raise NotImplementedError()

    @classmethod
    def results_reject(cls, websocket, message) -> None:
        raise NotImplementedError()

    @classmethod
    def results_error(cls, websocket, message) -> None:
        raise NotImplementedError()
