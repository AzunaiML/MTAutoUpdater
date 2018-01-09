import time

import schedule

from autoupdater.client import sender

sender_instance = sender.Sender()


def job():
    pass


def create_schedule(json):
    for i in json:
        sender_instance.send(i)
    pass



schedule.every().day.at("10:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
