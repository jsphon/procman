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


class ExitHandler(Thread):
    """ Class for handling exit signals"""

    def __init__(self, on_exit):
        super(ExitHandler, self).__init__()
        self.on_exit = on_exit
        self._q = Queue()

        signal.signal(signal.SIGINT, self._handle_exit)
        signal.signal(signal.SIGTERM, self._handle_exit)

        self.start()

    def run(self):
        self._q.get()
        self.on_exit()

    def _handle_exit(self, signum, frame):
        self._q.put(signum)


if __name__ == '__main__':
    """ Example Usage """

    def disp(msg):
        with open('/tmp/grace.txt', 'a') as f:
            f.write(msg + '\n')
        print(msg)

    def on_exit():
        disp('Gracefully Exiting')

    handler = ExitHandler(on_exit)

    def worker():
        while True:
            disp('%s Worker Doing work' % datetime.utcnow())
            time.sleep(1)

    t = Thread(target=worker)
    t.setDaemon(True)
    t.start()