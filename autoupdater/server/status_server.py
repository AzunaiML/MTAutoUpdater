import time
import os

from autoupdater.server import abstract_server


class StatusServer(abstract_server.AbstractServer):

    @staticmethod
    def check_status(path):
        return path

    def on_request(self, ch, method, props, body):
        status = self.check_status(body)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.write_queue,
                                   body=status)
        time.sleep(1)