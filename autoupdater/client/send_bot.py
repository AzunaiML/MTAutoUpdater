import telebot
import pika
import json
from autoupdater import config

connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.host))

channel = connection.channel()

bot = telebot.TeleBot(config.token)


def on_request(ch, method, props, body):
    body = body.decode('utf-8')
    message = json.loads(body)
    print(message)
    send_message(message['chat_id'], message['answer'])


def send_message(chat_id, text):
    bot.send_message(chat_id, text)


channel.basic_consume(on_request, queue=config.answer_queue_name)
channel.start_consuming()
