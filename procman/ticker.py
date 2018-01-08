import threading
import time


class Ticker(threading.Thread):
    def __init__(self, callback=None, delay=1.0):
        super(Ticker, self).__init__()
        self.callback = callback
        self.delay = delay
        self.isRunning = False

    def run(self):

        self.isRunning = True
        while self.isRunning:
            if self.callback:
                try:
                    self.callback()
                except Exception as e:
                    print(e)
            sleep_time = self.delay - (time.time() % self.delay)
            time.sleep(sleep_time)

    def stop(self):
        self.isRunning = False


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

    def stop(self):
        self.timer.cancel()


if __name__ == '__main__':

    def exampleCallback():
        print('callback at %s' % str(time.time()))

    ticker = Ticker(delay=0.5, callback=exampleCallback)
    ticker.start()

    time.sleep(2)

    ticker.stop()
