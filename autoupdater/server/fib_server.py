import time
import json
from autoupdater import config
from autoupdater.server import abstract_server


class FibServer(abstract_server.AbstractServer):
    def fib(self, n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.fib(n - 1) + self.fib(n - 2)

    def on_request(self, ch, method, props, body):
        body = body.decode('utf-8')
        message = json.loads(body)
        n = int(message['n'])
        time.sleep(1)
        print(" [.] fib(%s)" % n)
        response = {"fib": self.fib(n), "chat_id": message["chat_id"]}
        ch.basic_publish(exchange='',
                         routing_key=self.write_queue,
                         body=json.dumps(response))

        ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    fs = FibServer(config.host, config.task_queue_name, config.answer_queue_name)
    fs.run()