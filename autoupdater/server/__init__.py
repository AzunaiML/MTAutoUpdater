import autoupdater.config as config
from autoupdater.server import work_server as ws

if __name__ == '__main__':
    fs = ws.WorkServer(config.host,
                       config.task_queue_name,
                       config.answer_queue_name,
                       config.log_queue_name)
    fs.run()