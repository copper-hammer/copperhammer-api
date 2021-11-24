import tornado.web

from DB import DB
from Processings.ScannerProcessing import ScannerProcessing


class StatusServer(tornado.web.RequestHandler):
    def initialize(self, db: DB):
        self.__DB = db

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self, *args):
        return self.TestStatus()

    def TestStatus(self):
        self.set_status(200)
        mapping = {
            "result": {
                "status": "OK",
                "version": "0.0.3",
                "activeWebsockets":
                list(ScannerProcessing.list_alwss(self.__DB)),
            },
            "error": {
                "fr": False,
                "msg": None
            },
        }
        self.write(mapping)
