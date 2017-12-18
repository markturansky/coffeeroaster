import pyfirmata, os, copy, time, threading, os.path

jsTemplateFileLastModDate = 0
template = ""
jsTemplate = ""
jsTemplateTimestamp = 0

currentSpecFileLastModDate = 0

THERMO_ENV_DATA = 0x0A
THERMO_BEAN_DATA = 0x0B

class Roast:
    def __init__(self, bean, targetRoastLevel, targetTemperature):
        self.bean = bean
        self.targetRoastLevel = targetRoastLevel
        self.targetTemperature = targetTemperature
        self.timestamp = time.gmtime()
        self.data = []

    def add(self, snapshot):
        self.data.append([time.time(), snapshot])

class Roaster:
    """
    RoasterBoard is an Arduino firmata client communicating with the hardware roaster itself.
    """
    def __init__(self):
        print "initializing board"
        self.envTemp = 0
        self.beanTemp = 0
        self.lastEnvTemp = 0
        self.lastBeanTemp = 0

        # all roaster tuples are pin/spec
        self.components = {
            "heater": (13, 0),
            "drawfan": (12, 0),
            "scrollfan": (11, 0),
            "light": (8, 0),
            "drum": (9, 0)
        }
        self.loadBoard()

        self.thread = None
        self.roast = None
        self.isRoasting = False

    def roastIt(self, roast):
        if self.roast == None and self.isRoasting == False:
            self.roast = roast
            self.isRoasting = True
            self.thread = threading.Thread(name=self.roast.bean, target=self.run)
            self.thread.start()

    def run(self):
        isRunning = True
        while isRunning:
            # loop in 10s chunks of time
            for i in range(10):
                isRunning, specData = refreshSpec("roaster.spec")
                if isRunning == False:
                    break
                for key in specData:
                    desiredValue = specData[key]
                    self.setWhenDifferent(key, desiredValue)
                self.reconcile(i)
                snapshot = self.snapshot()
                self.roast.add(snapshot)
                time.sleep(1)
        self.isRoasting = False

    def snapshot(self):
        snapshot = copy.deepcopy(self.components)
        snapshot["envTemp"] = self.envTemp
        snapshot["beanTemp"] = self.beanTemp
        return snapshot

    def currentTemps(self):
        return self.envTemp, self.beanTemp

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
                print "%s compoent spec change from %s to %s" % (key, currentValue, desiredValue)
                self.components[key] = (pin, desiredValue)
        else:
            print "roaster has no component: %s", key


    def addEnvTemp(self, temp):
        avg = (self.lastEnvTemp + temp) / 2
        self.envTemp = avg
        self.lastEnvTemp = temp

    def addBeanTemp(self, temp):
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
            raise "no serial path found for roaster"

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

        print "found %s" % path
        board = pyfirmata.Arduino(path)

        # custom firmata events from arduino that sends temperature data to this python controller
        board.add_cmd_handler(THERMO_ENV_DATA, printEnv)
        board.add_cmd_handler(THERMO_BEAN_DATA, printBean)

        for c in self.components:
            board.digital[self.components[c][0]].mode = pyfirmata.OUTPUT
        board.digital[13].mode = pyfirmata.OUTPUT

        it = pyfirmata.util.Iterator(board)
        it.start()

        self.board = board

    def exit(self):
        for c in self.components:
            self.board.digital[self.components[c][0]].write(0)
        self.board.exit()

def refreshSpec(roasterSpec):
    global currentSpecFileLastModDate
    isRunning = True
    actualLastModDate = os.path.getmtime(roasterSpec)
    components = {}
    if actualLastModDate > currentSpecFileLastModDate:
        print "refresh the spec"
        with open(roasterSpec, 'r') as content_file:
            specdata = content_file.read()
        currentSpecFileLastModDate = actualLastModDate
        specdata = eval(specdata)
        for key in specdata:
            if key == "isRunning":
                isRunning = specdata[key]
            else:
                components[key] = specdata[key]
    return isRunning, components
