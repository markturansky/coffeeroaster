from pyfirmata import Arduino, util, OUTPUT
import time, sys, copy, os.path

THERMO_ENV_DATA = 0x0A
THERMO_BEAN_DATA = 0x0B

#board = Arduino("/dev/cu.wchusbserial1420")b
board = Arduino("/dev/ttyUSB0")

isRunning = True
specFileLastModDate = 0
jsTemplateFileLastModDate = 0
template = ""
timer = 0
roastdata = []
normalizingAmount = 0

def refreshSpec():
    global isRunning, specFileLastModDate
    lastmod = os.path.getmtime('roaster.spec')
    if lastmod > specFileLastModDate:
        print "refresh the spec"
        with open('roaster.spec', 'r') as content_file:
            specdata = content_file.read()
        specFileLastModDate = time.time()     
        specdata = eval(specdata)
        for key in specdata:
            if components.has_key(key):
                components[key]["Spec"] = specdata[key]
            elif key == "isRunning":
                isRunning = specdata[key]

def loadGraphTemplateJS():
    global template, jsTemplateFileLastModDate
    lastmod = os.path.getmtime('jstemplate.tmpl')
    if lastmod > jsTemplateFileLastModDate:
        with open('jstemplate.tmpl', 'r') as content_file:
            template = content_file.read()
    return template

def saveGraphData():
    global roastdata
    template = loadGraphTemplateJS()
    
    temperatures = []
    beantemps = []
    counter = 0
    for r in roastdata:
        timestamp = r[0]
        bt = r[1]["BeanTemp"]["Status"]
        et = r[1]["EnvTemp"]["Status"]
        temperatures.append([counter, et])
        beantemps.append([counter, bt])
        counter = counter + 1
    with open("webapp/startbootstrap-sb-admin-2-gh-pages/data/roasterdata.js", "w") as output:
        out = template.replace("$DATA", str(temperatures))
        out = out.replace("$BEANDATA", str(beantemps))
        output.write(out)
        output.flush()

def normalizeTemps():
    global normalizingAmount
    env = components["EnvTemp"]["Status"]
    bean = components["BeanTemp"]["Status"] = temp
    normalizingAmount = env - bean
    
def printEnv(*args, **kwargs):
    temp = args[0]
    temp = temp + args[1] * 128
    temp = temp + args[2] * 256
    temp = temp + args[3] * 512
    temp = temp - normalizingAmount
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
    "LightRelay": {
        "Pin": 8,
        "Spec": 1,
        "Status": 0,
    },
    "DrumRelay": {
        "Pin": 9,
        "Spec": 1,
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

if isRunning == False:
    normalizeTemps()
    isRunning = True
    
while isRunning:
    for i in range(10):
        refreshSpec()
        envTemp = components["EnvTemp"]["Status"]
        beanTemp = components["BeanTemp"]["Status"]

        if components.has_key("TargetTemp"):
            print "target temp ", components["TargetTemp"]
        
        for c in components:
            if components[c].has_key("Pin") and components[c].has_key("Spec"):
                port = components[c]["Pin"]
                onOff = pwm_profile[components[c]["Spec"]][i]
                if components[c]["Spec"] != components[c]["Status"]:
                    print c, "Diff!", components[c]["Spec"], components[c]["Status"]
                board.digital[port].write(onOff)
                components[c]["Status"] = components[c]["Spec"]
        timer = timer + 1
        snapshot = copy.deepcopy(components)
        if i % 10 == 0:
            print envTemp, beanTemp
        roastdata.append([time.time(), snapshot])
        saveGraphData()
        time.sleep(1)

for c in components:
    if components[c].has_key("Pin"):
        board.digital[components[c]["Pin"]].write(0)

board.exit()
