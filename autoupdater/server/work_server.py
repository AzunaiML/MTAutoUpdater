import time
import os
import json

from autoupdater.server import abstract_server


class WorkServer(abstract_server.AbstractServer):

    def do_job(self, task):
        pass

    def on_request(self, ch, method, props, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        result = self.do_job(body)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.write_queue,
                                   body=result)
        time.sleep(1)