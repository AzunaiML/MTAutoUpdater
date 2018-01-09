from autoupdater.server import log_server, status_server, work_server
from autoupdater import config
import multiprocessing
import time

# Реализовать запись в лог о том, что сервера запущены??


def logger(num):
    print("Logger created: ", num)
    return log_server.LogServer(config.host,
                                config.log_queue_name)


def status_checker(num):
    print("Status checker created", num)
    return status_server.StatusServer(config.host,
                                      config.status_queue_name,
                                      config.answer_queue_name)


def worker(num):
    print("Worker created", num)
    return work_server.WorkServer(config.host,
                                  config.task_queue_name,
                                  config.answer_queue_name,
                                  config.log_queue_name)


if __name__ == '__main__':
    jobs = []
    for i in range(config.log_servers):
        p = multiprocessing.Process(target=logger, args=(i,))
        jobs.append(p)
        p.start()

    for i in range(config.status_servers):
        p = multiprocessing.Process(target=status_checker, args=(i,))
        jobs.append(p)
        p.start()

    for i in range(config.work_servers):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()

    time.sleep(20)
    for i in jobs:
        i.terminate()