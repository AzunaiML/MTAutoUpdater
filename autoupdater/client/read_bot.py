import telebot
import json
import autoupdater.client.sender as b
from autoupdater import config
import time
import threading


def load_name_command(path):
    json_f = json.load(open(path))
    root = [i for i in json_f][0]
    tasks = [i for i in json_f[root]]
    commands = []
    for i in range(len(tasks)):
        commands.append({'task': tasks[i], 'command': json_f[root][tasks[i]]["command"]})
    return commands


def send_message(chat_id, text):
    bot.send_message(chat_id, text)


bot = telebot.TeleBot(config.token)
tasks = load_name_command(config.tasks_json_path)
statuses = load_name_command(config.statuses_json_path)
tasks_commands = [i["command"] for i in tasks]
statuses_commands = [i["command"] for i in statuses]


@bot.message_handler(commands=['test', 'help'])
def send_welcome(message):
    client = b.Sender()
    send_message(message.chat.id, "Hi!")
    m = {'n': 10, "chat_id": message.chat.id}
    client.send(m, config.task_queue_name)


@bot.message_handler(commands=tasks_commands)
def read_tasks(message):
    client = b.Sender()
    text = message.text[1:]
    task_name = ""
    for i in tasks:
        if i["command"] == text:
            task_name = i["task"]
    json_f = json.load(open(config.tasks_json_path))
    root = [i for i in json_f][0]
    task_content = json_f[root][task_name]
    task = {"chat_id": message.chat.id,
            "task-name": task_name,
            "task": task_content}
    client.send(task, config.task_queue_name)


@bot.message_handler(commands=statuses_commands)
def read_statuses(message):
    client = b.Sender()
    status = {}
    client.send(status, config.status_queue_name)


def bot_start():
    while True:
        try:
            time.sleep(5)
            bot.polling(timeout=60, interval=0, none_stop=False)
        except Exception as e:
            print(e)
        print('sleep')
        time.sleep(1)


if __name__ == '__main__':
    threads = {
        'bot': threading.Thread(target=bot_start)
    }
    threads['bot'].start()
    while True:
        for t, f in threads.items():
            if not f.is_alive:
                print(t, ' умер, перезапускаю')
                f.start()
        time.sleep(1)
