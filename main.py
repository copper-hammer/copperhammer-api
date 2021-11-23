from pathlib import Path
from re import I, S

import tornado.ioloop
import tornado.web
import tornado.websocket

from config import Config
from DB import DB
from Servers.StatusServer import StatusServer
from Sockets.ScannerSocket import ScannerSocket

_CONFIG = Config(Path("config.ini"))

db = DB(
    host=_CONFIG.get("MongoDB", "host"),
    port=int(_CONFIG.get("MongoDB", "port")),
    username=_CONFIG.get("MongoDB", "username"),
    password=_CONFIG.get("MongoDB", "password"),
)


def mapp():
    urls = [
        (r"/status", StatusServer),
        (r"/scanner/ws", ScannerSocket, {
            "db": db
        }),
    ]
    return tornado.web.Application(urls,
                                   debug=True,
                                   websocket_ping_interval=2,
                                   websocket_ping_timeout=10)


if __name__ == "__main__":
    app = mapp()
    app.listen(int(_CONFIG.get("WebServer", "port")))
    tornado.ioloop.IOLoop.instance().start()
