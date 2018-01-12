import pika
from abc import ABC, abstractmethod


class AbstractServer(ABC):
    def __init__(self, host, read_queue, write_queue=None, log_queue=None, prefetch_count=1):
        self.read_queue = read_queue
        self.write_queue = write_queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=read_queue)

        if write_queue is not None:
            self.channel.queue_declare(queue=write_queue)
        if log_queue is not None:
            self.channel.queue_declare(queue=log_queue)
        self.channel.basic_qos(prefetch_count=prefetch_count)

    @abstractmethod
    def on_request(self, ch, method, props, body):
        pass

    def send_log(self, message):
        pass

    def run(self):
        self.channel.basic_consume(self.on_request, queue=self.read_queue)
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()
