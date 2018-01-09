import telebot
import json
import autoupdater.client.sender as b
from autoupdater import config

client = b.Sender()
bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    send_message(message.chat.id, "Hi!")
    m = {'n': 10, "chat_id": message.chat.id}
    client.send(m, config.task_queue_name)


def send_message(chat_id, text):
    bot.send_message(chat_id, text)


if __name__ == '__main__':
    bot.polling(none_stop=True)