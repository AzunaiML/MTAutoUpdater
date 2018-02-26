import time
import os
import json
import pandas as pd
import codecs
import os
import pika
os.environ["NLS_LANG"] = "Russian.AL32UTF8"
import cx_Oracle
from autoupdater.server import abstract_server
import autoupdater.client.sender as b


class WorkServer(abstract_server.AbstractServer):

    def do_job(self, task):
        if task["type"] == "download":
            print("I got download task")
            return self.do_download(task["parameters"])
        elif task["type"] == "update":
            return self.do_update(task["parameters"])
        elif task["type"] == "upload":
            return self.do_upload(task["parameters"])
        else:
            return "Error - no such task type"

    def do_update(self, task):
        pass

    def do_download(self, task):
        try:
            file_obj = codecs.open(task["query"], "r", "utf_8_sig")
            query = file_obj.read()
            file_obj.close()
            connection = None
            if task["database-type"] == "oracle":
                connection = cx_Oracle.connect(user=task["user"],
                                               password=task["password"],
                                               dsn=task["connection-string"])
                print("connection established")
                # Write log about connection
                self.send_log("")
            else:
                pass
            df = pd.read_sql(query, connection)
            print("done")
            df.to_excel(task["destination"]["file-path"]+task["destination"]["file-type"], index=False)
            answer = "File: " + str(task["destination"]["file-path"]+task["destination"]["file-type"]) + " was downloaded"

            # Write log about file
            self.send_log("")
        except Exception as e:
            answer = "Error: " + str(e)
            print(answer)
            # Write log about error
            self.send_log("")
        return answer

    def do_upload(self, task):
        pass

    def reconnect(self):
        """Will be invoked by the IOLoop timer if the connection is
        closed. See the on_connection_closed method.

        """
        self.connection.close()

        if not self._closing:
            # Create a new connection
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, heartbeat=0))

    def on_request(self, ch, method, props, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        result = self.do_job(body["task"])
        answer = {"chat_id": body["chat_id"], "answer": result, "task-name": body["task-name"]}
        print(answer)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.write_queue,
                                   body=json.dumps(answer))
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def on_connection_closed(self, connection, reply_code, reply_text):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param int reply_code: The server provided reply_code if given
        :param str reply_text: The server provided reply_text if given

        """
        self.channel = None
        if self._closing:
            self.connection.close()
        else:
            self.connection.add_timeout(5, self.reconnect)


