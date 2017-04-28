import threading
import time


class Ticker(threading.Thread):
    def __init__(self, callback=None, delay=1.0):
        super(Ticker, self).__init__()
        self.callback = callback
        self.delay = delay

    def run(self):

        while True:
            if self.callback:
                try:
                    self.callback()
                except Exception as e:
                    print(e)
            sleep_time = self.delay - (time.time() % self.delay)
            print(time.time())
            time.sleep(sleep_time)


if __name__ == '__main__':
    ticker = Ticker(delay=0.1)
    ticker.setDaemon(True)
    ticker.start()

    time.sleep(1)

