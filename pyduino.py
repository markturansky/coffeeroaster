from pyfirmata import Arduino, util, INPUT
import time

board = Arduino("/dev/cu.wchusbserial1420")
it = util.Iterator(board)
it.start()

board.digital[5].mode = INPUT
board.digital[5].enable_reporting()
board.digital[6].mode = INPUT
board.digital[6].enable_reporting()
board.digital[7].mode = INPUT
board.digital[7].enable_reporting()

board.analog[1].enable_reporting()

components = [
    ("Heater", 8, 11),
    ("ScrollFan", 9, 12),
    ("DrawFan", 10, 13),
    ("Temp", 1)
]

isHeaterOn = False
isDrawFanOn = False
isScrollFanOn = False
lastPoll = 0

def write(pin, value):
    board.digital[pin].write(value)

def readA(pin):
    return board.analog[pin].read()

def readD(pin):
    return board.digital[pin].read()


while True:
    board.iterate()

    heaterBtn = readD(5)
    scrollBtn = readD(6)
    drawBtn = readD(7)

    if heaterBtn == True:
        heater = components[0]
        if isHeaterOn:
            isHeaterOn = False
        else:
            isHeaterOn = True
        write(heater[1], isHeaterOn)
        write(heater[2], isHeaterOn)

    if scrollBtn == True:
        scrollFan = components[1]
        if isScrollFanOn:
            isScrollFanOn = False
        else:
            isScrollFanOn = True
        write(scrollFan[1], isScrollFanOn)
        write(scrollFan[2], isScrollFanOn)

    if drawBtn == True:
        drawFan = components[2]
        if isDrawFanOn:
            isDrawFanOn = False
        else:
            isDrawFanOn = True
        write(drawFan[1], isDrawFanOn)
        write(drawFan[2], isDrawFanOn)

    rawvoltage= readA(components[3][1])
    if rawvoltage != None:
        millivolts= float((rawvoltage/1024.0) * 5000000)
        tempC = float(millivolts/10)
        tempF = (tempC * 9/5 + 32)
        # some readings go off the charts by thousands ... IDK why
        if tempF < 1000:
            print "mv {}  tempC {}  tempF {}".format(millivolts, tempC, tempF)

    time.sleep(1)
