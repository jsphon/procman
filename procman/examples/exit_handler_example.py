"""

Example from /usr/lib/systemd/system/grace.service

[Unit]
Description=grace

[Service]
Type=simple
Environment="PYTHONPATH=/srv/procman"
ExecStart=/opt/anaconda3/bin/python /srv/procman/procman/examples/exit_handler_example.py
User=jon
Restart=always

[Install]
WantedBy=graphical.target


"""

from procman.exit_handler import ExitHandler

from datetime import datetime
import time
from threading import Thread


def on_exit():
    disp('Gracefully Exiting')


def disp(msg):
    with open('/tmp/grace.txt', 'a') as f:
        f.write(msg + '\n')
    print(msg)

if __name__ == '__main__':
    ExitHandler(on_exit)

    def example_daemon():
        while True:
            disp('%s Daemon Doing work' % datetime.utcnow())
            time.sleep(1)

    t = Thread(target=example_daemon)
    t.setDaemon(True)
    t.start()
