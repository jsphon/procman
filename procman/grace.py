"""

Example from /usr/lib/systemd/system/grace.service

[Unit]
Description=grace

[Service]
Type=simple
ExecStart=/usr/bin/python /srv/procman/procman/grace.py
User=jon
Restart=always

[Install]
WantedBy=graphical.target

"""

from datetime import datetime
import signal
import time
from threading import Thread
from queue import Queue


class GracefulKiller(Thread):

    def __init__(self, on_exit):
        super(GracefulKiller, self).__init__()
        self.on_exit = on_exit
        self._q = Queue()

        signal.signal(signal.SIGINT, self._handle_exit)
        signal.signal(signal.SIGTERM, self._handle_exit)

    def run(self):
        self._q.get()
        self.on_exit()

    def _handle_exit(self, signum, frame):
        self._q.put(signum)


def on_exit():
    disp('Gracefully Exiting')


def disp(msg):
    with open('/tmp/grace.txt', 'a') as f:
        f.write(msg + '\n')
    print(msg)


if __name__ == '__main__':
    killer = GracefulKiller(on_exit)
    killer.start()

    def worker():
        while True:
            disp('%s Worker Doing work' % datetime.utcnow())
            time.sleep(1)

    t = Thread(target=worker)
    t.setDaemon(True)
    t.start()