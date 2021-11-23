import tornado.web

from Processings.ScannerProcessing import ScannerProcessing


class StatusServer(tornado.web.RequestHandler):
    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self, *args):
        return self.TestStatus()

    def TestStatus(self):
        self.set_status(200)
        ScannerProcessing.send_message("Test")
        mapping = {
            "result": {
                "status": "OK",
                "version": "0.0.3",
                "activeWebsockets": list(ScannerProcessing.list_alwss()),
            },
            "error": {
                "fr": False,
                "msg": None
            },
        }
        self.write(mapping)
