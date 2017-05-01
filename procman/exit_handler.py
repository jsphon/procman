from datetime import datetime
import signal
import time
from threading import Thread
from queue import Queue


class ExitHandler(Thread):
    """ Handles Exit Signals sent by the OS.
    This is particularly useful for services.
    See the examples/exit_handler_example.py for more details.
    """

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
