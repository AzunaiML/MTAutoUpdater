import time
import os
import json
import pandas as pd
import codecs
import os
os.environ["NLS_LANG"] = "Russian.AL32UTF8"
import cx_Oracle
from autoupdater.server import abstract_server


class WorkServer(abstract_server.AbstractServer):

    def do_job(self, task):
        pass

    def do_update(self, task):
        pass

    def do_download(self, task):
        answer = ""
        try:
            file_obj = codecs.open(task["query"], "r", "utf_8_sig")
            query = file_obj.read()
            file_obj.close()
            connection = None
            if task["database-type"] == "oracle":
                connection = cx_Oracle.connect(user=task["user"],
                                               password=task["password"],
                                               dsn=task["connection-string"])
                ## Write log about connection
            else:
                pass
            df = pd.read_sql(query, connection)
            df.to_excel(task["destination"]["file-path"]+task["destination"]["file-type"], index=False)
            answer = "File: " + str(task["destination"]["file-path"]+task["destination"]["file-type"]) + " was downloaded"
            ## Write log about file
        except Exception as e:
            answer = "Error: " + str(e)
            ## Write log about error
        return answer

    def do_upload(self, task):
        pass

    def on_request(self, ch, method, props, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        result = self.do_job(body["task"])
        self.channel.basic_publish(exchange='',
                                   routing_key=self.write_queue,
                                   body=result)
        time.sleep(1)