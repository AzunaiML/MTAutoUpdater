import pika
import json
from autoupdater import config


class Sender(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.host))
        self.channel = self.connection.channel()

    def send(self, message, queue):
        """
        :param queue: queue name where we want to send message
        :param message: json message (update/download/upload/log/answer) which pushes in task queue
        """
        self.channel.basic_publish(exchange='',
                                   routing_key=queue,
                                   body=json.dumps(message))
