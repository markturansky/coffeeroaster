import time

class Roast:
    def __init__(self, bean, targetRoastLevel, targetTemperature):
        self.bean = bean
        self.targetRoastLevel = targetRoastLevel
        self.targetTemperature = targetTemperature
        self.timestamp = time.gmtime()
        self.data = []

    def add(self, snapshot):
        self.data.append([time.time(), snapshot])
