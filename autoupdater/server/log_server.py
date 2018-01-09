import time

from autoupdater.server import abstract_server


class LogServer(abstract_server.AbstractServer):
    def write_log(self, message):
        pass

    def on_request(self, ch, method, props, body):
        self.write_log(body)
        time.sleep(1)