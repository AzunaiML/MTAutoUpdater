import time
import os
import json
from datetime import datetime

from autoupdater.server import abstract_server


class StatusServer(abstract_server.AbstractServer):
    @staticmethod
    def get_upd_date_file(path):
        return datetime.strftime(datetime.fromtimestamp(os.path.getmtime(path)), '%d.%m.%Y %H:%M:%S')

    @staticmethod
    def check_status(path):
        msg = ''
        for f in path:
            if os.path.exists(f):
                msg += "Файл %s: обновлен %s\n" % (os.path.split(f)[-1], str(StatusServer.get_upd_date_file(f)))
            else:
                msg += "Файл %s: не обновлен\n" % (os.path.split(f)[-1])
        return msg

    def on_request(self, ch, method, props, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        status = self.check_status(json.loads(body["path"]))
        response = {"status": status, "chat_id": body["chat_id"]}
        self.channel.basic_publish(exchange='',
                                   routing_key=self.write_queue,
                                   body=json.dumps(response))
        time.sleep(1)
