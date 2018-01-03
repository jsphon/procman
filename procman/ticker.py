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


class StoppableTicker(object):
    def __init__(self, callback=None, delay=1.0):
        super(StoppableTicker, self).__init__()
        self.callback = callback
        self.delay = delay
        self.timer = None

    def run(self):

        if self.callback:
            try:
                self.callback()
            except Exception as e:
                print(e)
        sleep_time = self.delay - (time.time() % self.delay)
        self.timer = threading.Timer(sleep_time, self.run)
        self.timer.start()
        print(time.time())

    def stop(self):
        self.timer.cancel()


if __name__ == '__main__':
    ticker = StoppableTicker(delay=0.5)
    ticker.run()

    time.sleep(2)

    ticker.stop()
