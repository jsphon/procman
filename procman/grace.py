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


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def disp(msg):
    with open('/tmp/grace.txt', 'a') as f:
        f.write(msg + '\n')
    print(msg)


if __name__ == '__main__':
    killer = GracefulKiller()
    while True:
        time.sleep(1)
        disp("%s doing something in a loop ..." % datetime.utcnow())

        if killer.kill_now:
            break

    with open('/tmp/grace.txt', 'a') as f:
        f.write('end of program, killed gracefully')
    print "End of the program. I was killed gracefully :)"
