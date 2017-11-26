from pyfirmata import Arduino, util, INPUT, PWM
import time

board = Arduino("/dev/cu.wchusbserial1420")
it = util.Iterator(board)
it.start()


board.analog[1].enable_reporting()

components = {
    "Heater": {
        "Pin": "d:6:p",  # digital : pin 6 : PWM
        "LED": 7,
        "Spec": 0,
        "Status": 0,
    },
    "DrawFan": {
        "PWM": "d:9:p",
        "LED": 8,
        "Spec": 0,
        "Status": 0,
    },
    "ScrollFan":{
        "PWM": "d:10:p",
        "LED": 12,
        "Spec": 0,
        "Status": 0,
    },
    "DrumMotor": {
        "PWM": "d:11:p",
        "LED": 13,
        "Spec": 0,
        "Status": 0,
    }
}

for name in components.keys():
    print "Setting %s to PWM" % name
    c = components[name]
    board.digital[c.PWM].mode = PWM

def measurements():
    rawvoltage = board.get_pin("a:1:i").read()
    if rawvoltage != None:
        millivolts= float((rawvoltage/1024.0) * 5000000)
        tempC = float(millivolts/10)
        tempF = (tempC * 9/5 + 32)
        # some readings go off the charts by thousands ... IDK why
        if tempF < 1000:
            print "mv {}  tempC {}  tempF {}".format(millivolts, tempC, tempF)

def reconcile():
    for name in components.keys():
        print "Reconciling %s" % name
        c = components[name]
        if c.Spec != c.Status:
            board.digital[c.PWM].write(c.Spec)
            c.Status = c.Spec
            print "  setting {} to {}".format(name, c.Spec)

def savestate():
    print "TODO: save to roast data"

while True:
    measurements()
    reconcile()
    savestate()
    time.sleep(1)
