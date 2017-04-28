import os
import threading
import time


def force_exit(delay=1.0):

    def target():
        time.sleep(delay)
        import os
        print('Force Exitting')
        os._exit(0)

    t = threading.Thread(target=target)
    t.setDaemon(True)
    t.start()


if __name__=='__main__':
    force_exit(1)