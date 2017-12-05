from pyfirmata import Arduino, util, OUTPUT, PinAlreadyTakenError
import time, sys

THERMO_ENV_DATA = 0x0A
THERMO_BEAN_DATA = 0x0B

#board = Arduino("/dev/cu.wchusbserial1420")
board = Arduino("/dev/ttyUSB1")

isRunning = True
timer = 0
roastdata = []

def refreshSpec():
    global isRunning
    with open('roaster.spec', 'r') as content_file:
        specdata = content_file.read()
    specdata = eval(specdata)
    for key in specdata:
        if components.has_key(key):
            components[key]["Spec"] = specdata[key]
        elif key == "isRunning":
            isRunning = specdata[key]

def saveGraphData():
    template = """//Flot Line Chart
$(document).ready(function() {

    var offset = 0;
    plot();

    function plot() {
        var heater = $DATA;

        var options = {
            series: {
                lines: {
                    show: true
                },
                points: {
                    show: true
                }
            },
            grid: {
                hoverable: true //IMPORTANT! this is needed for tooltip to work
            },
            yaxis: {
                min: 0,
                max: 500,
            },
            tooltip: true,
            tooltipOpts: {
                content: "'%s' of %x.1 is %y.4",
                shifts: {
                    x: -60,
                    y: 25
                }
            }
        };

        var plotObj = $.plot($("#roast-line-chart"), [{
                data: heater,
                label: "heater (F)"
            }],
            options);
    }
});
"""
    temperatures = []
    counter = 0
    for r in roastdata:
        t = r["EnvTemp"]["Status"]
        temperatures.append([counter, t])
        counter = counter + 1
    with open("webapp/startbootstrap-sb-admin-2-gh-pages/data/roasterdata.js", "w") as output:
        out = template.replace("$DATA", str(temperatures))
        output.write(out)
        output.flush()

def printEnv(*args, **kwargs):
    temp = args[0]
    temp = temp + args[1] * 128
    temp = temp + args[2] * 256
    temp = temp + args[3] * 512
    components["EnvTemp"]["Status"] = temp

def printBean(*args, **kwargs):
    temp = args[0]
    temp = temp + args[1] * 128
    temp = temp + args[2] * 256
    temp = temp + args[3] * 512    
    components["BeanTemp"]["Status"] = temp

board.add_cmd_handler(THERMO_ENV_DATA, printEnv )
board.add_cmd_handler(THERMO_BEAN_DATA, printBean )


components = {
    "Heater": {
        "Pin": 13,
        "Spec": 3,
        "Status": 0,
    },
    "DrawFan": {
        "Pin": 12,
        "Spec": 10,
        "Status": 0,
    },
    "ScrollFan":{
        "Pin": 11,
        "Spec": 6,
        "Status": 0,
    },
    "DrumMotor": {
        "Pin": 9,
        "Spec": 8,
        "Status": 0,
    },
    "EnvTemp": {
        # "Pin" is not applicable
        "Spec": 0, # desired environment temperature
        "Status": 0, # actual environment temperature
    },
    "BeanTemp": {
        # "Pin" is not applicable
        # "Spec" is not applicable.
        "Status": 0, # actual bean temperature
    },
}

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


it = util.Iterator(board)
it.start()

# setup
for c in components:
    if components[c].has_key("Pin"):
        port = components[c]["Pin"]
        pin = board.digital[port].mode = OUTPUT
board.digital[13].mode = OUTPUT

# loop in 10s chunks of time

while isRunning:
    for i in range(10):
        refreshSpec()
        envTemp = components["EnvTemp"]["Status"]
        beanTemp = components["BeanTemp"]["Status"]

        if components.has_key("TargetTemp"):
            print "target temp ", components["TargetTemp"]
        
        for c in components:
            if components[c].has_key("Pin"):
                port = components[c]["Pin"]
                onOff = pwm_profile[components[c]["Spec"]][i]
                board.digital[port].write(onOff)
                components[c]["Status"] = int(onOff)
        timer = timer + 1
        snapshot = components.copy()
        if i % 10 == 0:
            print snapshot
        roastdata.append(snapshot)
        saveGraphData()
        time.sleep(.5)

for c in components:
    if components[c].has_key("Pin"):
        board.digital[components[c]["Pin"]].write(0)

board.exit()
