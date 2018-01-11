import telebot
import json
import autoupdater.client.sender as b
from autoupdater import config


def load_commands(path):
    json_f = json.load(open(path))
    root = [i for i in json_f][0]
    return [i for i in json_f[root]]


def send_message(chat_id, text):
    bot.send_message(chat_id, text)

client = b.Sender()
bot = telebot.TeleBot(config.token)
tasks_commands = load_commands(config.tasks_json_path)
statuses_commands = load_commands(config.statuses_json_path)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    send_message(message.chat.id, "Hi!")
    m = {'n': 10, "chat_id": message.chat.id}
    client.send(m, config.task_queue_name)


@bot.message_handler(commands=tasks_commands)
def read_tasks(message):
    task = {}
    client.send(task, config.task_queue_name)


@bot.message_handler(commands=statuses_commands)
def read_statuses(message):
    status = {}
    client.send(status, config.status_queue_name)


if __name__ == '__main__':
    bot.polling(none_stop=True)
