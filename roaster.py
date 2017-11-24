from threading import Thread, Condition
from time import sleep

class ApiServer:
    def __init__(self):
        self.name = "Smart Roaster API Server"
        self.thread = None
        self.running = True

    def start(self):
        self.thread = Thread(name=self.name, target=self.run)
        self.thread.start()

    def run(self):
        while self.running:
            print "hi api"
            sleep(1)

    def stop(self):
        self.running = False

class RoastComponent():
    def __init__(self, name, pin):
        """
        :param name: the name of roaster component (e.g, heater)
        :param pin: the GPIO pin on the Pi
        :param condition: the condition used to wait/notify this component of changes
        :return:
        """
        self.name = name
        self.pin = pin
        self.condition = Condition()
        self.running = False
        self.thread = None

    def start(self):
        if self.running == False:
            self.running = True
            # self.thread = Thread(target=self.run, name=self.name)
            # self.thread.start()

    def stop(self):
        if self.running == True:
            self.running = False
            self.condition.acquire()
            self.condition.notify()
            self.condition.release()

    def poll(self):
        if self.running:
            self.condition.acquire()
            self.condition.notify()
            self.condition.release()

    def run(self):
        while self.running:
            self.condition.acquire()
            self.condition.wait()
            print "{} hello world, love {}".format(self.pin, self.name)
            self.condition.release()


if __name__ == '__main__':
    components = [
        RoastComponent(name="Heater", pin=6),
        RoastComponent(name="Draw Fan", pin=7),
        RoastComponent(name="Scroll Fan", pin=8),
        RoastComponent(name="Drum Motor", pin=9),
    ]

    # for c in components:
    #     print c
    #     c.start()
    #
    # for i in range(10):
    #     for c in components:
    #         c.poll()
    #
    # for c in components:
    #     c.stop()

    api = ApiServer()
    api.start()

    sleep(13)

    api.stop()
