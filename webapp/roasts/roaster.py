import pyfirmata, os, time, threading, os.path, sys

from roasts.models import Roast, RoastSnapshot

THERMO_ENV_DATA = 0x0A
THERMO_BEAN_DATA = 0x0B

def debug(str):
    print str

class Roaster:
    """
    RoasterBoard is an Arduino firmata client communicating with the hardware roaster itself.
    """
    def __init__(self):
        self.envTemp = 0
        self.beanTemp = 0
        self.lastEnvTemp = 0
        self.lastBeanTemp = 0

        # all roaster tuples are pin/spec
        self.components = {
            "heater": (13, 0),
            "drawfan": (12, 0),
            "scrollfan": (11, 0),
            "light": (8, 10),
            "drum_low": (9, 0),
            "drum_high": (10, 0)
        }
        self.thread = None
        self.roast = None
        self.isRoasting = False
        self.board = None

    def start(self):
        self.thread = threading.Thread(name="roaster", target=self.run)
        self.thread.start()
        self.isRoasting = True

    def stop(self):
        self.isRoasting = False

    def run(self):
        debug("loading Arduino")
        self.loadBoard()

        while self.isRoasting:
            # loop in 10s chunks of time
            for i in range(10):
                roast = None
                results = Roast.objects.filter(is_active_roast=1)
                if results:
                    roast = results[0]

                # starting a new roast
                if self.roast == None and roast:
                    debug("New roast!")
                    self.roast = roast

                # the previously running roast was stopped
                if self.roast and not roast:
                    debug("Previously running roast was stopped")
                    self.roast = None
                    break

                # get out of this loop if no active roast
                if not roast:
                    debug("No roast. All off.")
                    time.sleep(1)
                    self.setWhenDifferent("heater", 0)
                    self.setWhenDifferent("drawfan", 0)
                    self.setWhenDifferent("scrollfan", 0)
                    self.setWhenDifferent("heater", 0)
                    self.setWhenDifferent("drum_low", 0)
                    self.setWhenDifferent("drum_high", 0)
                    self.reconcile(0)
                    break

                heater = roast.heater if roast.heater else 0
                drawfan = roast.drawfan if roast.drawfan else 0
                scrollfan = roast.scrollfan if roast.scrollfan else 0
                drum = roast.drum if roast.drum else 0
                env_temp = self.envTemp
                bean_temp = self.beanTemp

                print "heater = %s drawfan = %s scrollfan = %s drum = %s, env_temp = %s bean_temp = %s" % (heater, drawfan, scrollfan, drum, env_temp, bean_temp)

                self.setWhenDifferent("heater", heater)
                self.setWhenDifferent("drawfan", drawfan)
                self.setWhenDifferent("scrollfan", scrollfan)
                self.setWhenDifferent("heater", heater)

                # stop drum
                if drum == 0:
                    self.setWhenDifferent("drum_low", 0)
                    self.setWhenDifferent("drum_high", 0)
                # low
                if drum == 1:
                    self.setWhenDifferent("drum_low", 10)
                    self.setWhenDifferent("drum_high", 0)
                # high
                if drum == 2:
                    self.setWhenDifferent("drum_low", 0)
                    self.setWhenDifferent("drum_high", 10)

                self.reconcile(i)

                snapshot = RoastSnapshot(roast=roast, heater=heater, drawfan=drawfan, scrollfan=scrollfan, drum=drum, env_temp=env_temp, bean_temp=bean_temp)
                snapshot.save()
                time.sleep(1)
        self.board.exit()

    def reconcile(self, tick=0):
        pwm_profile = [
            [0,0,0,0,0,0,0,0,0,0], # 0 -- all off
            [1,0,0,0,0,0,0,0,0,0], # 1 -- on 10%
            [1,0,0,0,0,1,0,0,0,0], # 2 -- on 20%
            [1,0,0,1,0,0,1,0,0,0], # 3 -- on 30%
            [1,0,0,1,0,0,1,0,0,1], # 4 -- on 40%
            [1,0,1,0,1,0,1,0,1,0], # 5 -- on 50%
            [1,1,1,0,1,0,1,0,1,0], # 6 -- on 60%
            [1,1,1,0,1,0,1,1,1,0], # 7 -- on 70%
            [1,1,1,1,1,0,1,1,1,0], # 8 -- on 80%
            [1,1,1,1,1,1,1,1,1,0], # 9 -- on 90%
            [1,1,1,1,1,1,1,1,1,1], # 10 -- on 100%
        ]
        for key in self.components:
            pin, value = self.components[key]
            onOff = pwm_profile[value][tick]
            self.board.digital[pin].write(onOff)

    def setWhenDifferent(self, key, desiredValue):
        if self.components.has_key(key):
            pin, currentValue = self.components[key]
            if desiredValue != currentValue:
                print "%s spec change from %s to %s" % (key, currentValue, desiredValue)
                self.components[key] = (pin, desiredValue)
        else:
            print "roaster has no component: %s", key

    def addEnvTemp(self, temp):
        if self.lastEnvTemp == 0:
            self.lastEnvTemp = temp
        avg = (self.lastEnvTemp + temp) / 2
        self.envTemp = avg
        self.lastEnvTemp = temp

    def addBeanTemp(self, temp):
        if self.lastBeanTemp == 0:
            self.lastBeanTemp = temp
        avg = (self.lastBeanTemp + temp) / 2
        self.beanTemp = avg
        self.lastBeanTemp = temp

    def loadBoard(self):
        serialPath = ""
        for i in range(5):
            # osx paths for arduino
            path = "/dev/cu.wchusbserial142%s" % i
            if os.path.exists(path):
                serialPath = path
                break
            # raspberry pi paths for arduino
            path = "/dev/ttyUSB%s" % i
            if os.path.exists(path):
                serialPath = path
                break

        if serialPath == "":
            raise Exception("no serial path found for roaster")

        def getTemp(args):
            temp = args[0]
            temp = temp + args[1] * 128
            temp = temp + args[2] * 256
            temp = temp + args[3] * 512
            return temp

        def printEnv(*args, **kwargs):
            self.addEnvTemp(getTemp(args))

        def printBean(*args, **kwargs):
            self.addBeanTemp(getTemp(args))

        print "using %s" % path
        self.board = pyfirmata.Arduino(path)

        # custom firmata events sent from arduino contains temperature data
        self.board.add_cmd_handler(THERMO_ENV_DATA, printEnv)
        self.board.add_cmd_handler(THERMO_BEAN_DATA, printBean)

        for c in self.components:
            self.board.digital[self.components[c][0]].mode = pyfirmata.OUTPUT
        self.board.digital[13].mode = pyfirmata.OUTPUT

        it = pyfirmata.util.Iterator(self.board)
        it.start()


