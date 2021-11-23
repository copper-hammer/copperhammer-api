from DB import DB
from Types import APIKeyTypes


class ScannerProcessing:
    __alws = []

    def __init__(self) -> None:
        pass

    @classmethod
    def add_lws(cls, websocket) -> None:
        cls.__alws.append(websocket)
        websocket.isBusy = False

    def remove_nonworking_sockets(self) -> None:
        to_be_removed = set()
        for websocket in self.__alws:
            if not websocket.ws_connection or not websocket.ws_connection.stream.socket:
                to_be_removed.add(websocket)
        for websocket in to_be_removed:
            self.__alws.remove(websocket)

    @classmethod
    def list_alwss(cls) -> list:
        cls.remove_nonworking_sockets(cls)
        for vsocket in cls.__alws:
            yield {
                "nodeName": None,
                "isBusy": vsocket.isBusy,
                "socketObject": str(vsocket),
            }

    @classmethod
    def send_message(cls, message) -> int:
        cls.remove_nonworking_sockets(cls)
        for vsocket in cls.__alws:
            if not vsocket.isBusy:
                vsocket.isBusy = True
                vsocket.send_message(message)
                return 1
        return 0

    @staticmethod
    def set_node_id(wbo) -> None:
        raise NotImplementedError()

    @staticmethod
    def authenticate_request(wbo) -> None:
        raise NotImplementedError()

    @staticmethod
    def authenticate_accept(wbo) -> None:
        raise NotImplementedError()

    @staticmethod
    def authenticate_reject(wbo) -> None:
        raise NotImplementedError()

    @staticmethod
    def authenticate_error(wbo) -> None:
        raise NotImplementedError()

    @staticmethod
    def yagood_node(wbo) -> None:
        raise NotImplementedError()

    @staticmethod
    def send_batch(wbo) -> None:
        raise NotImplementedError()

    @staticmethod
    def batch_accept_confirm(wbo) -> None:
        raise NotImplementedError()

    @staticmethod
    def submit_results(wbo) -> None:
        raise NotImplementedError()

    @staticmethod
    def results_accept_confirm(wbo) -> None:
        raise NotImplementedError()

    @staticmethod
    def results_reject(wbo) -> None:
        raise NotImplementedError()

    @staticmethod
    def results_error(wbo) -> None:
        raise NotImplementedError()
