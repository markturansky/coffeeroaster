import os.path

jsTemplateFileLastModDate = 0
template = ""
jsTemplate = ""
jsTemplateTimestamp = 0

currentSpecFileLastModDate = 0

def loadGraphTemplateJS(path, currentContent="", currentLastModDate=0):
    actualLastModDate = os.path.getmtime(path)
    if actualLastModDate > currentLastModDate:
        with open(path, 'r') as content_file:
            currentContent = content_file.read()
    return currentContent, actualLastModDate

def saveGraphData(roastdata):
    global jsTemplate, jsTemplateTimestamp
    jsTemplate, jsTemplateTimestamp = loadGraphTemplateJS("jstemplate.tmpl", jsTemplate, jsTemplateTimestamp)

    temperatures = []
    beantemps = []
    counter = 0
    for r in roastdata:
        timestamp = r[0]
        bt = r[1]["beanTemp"]
        et = r[1]["envTemp"]
        temperatures.append([counter, et])
        beantemps.append([counter, bt])
        counter = counter + 1
    with open("webapp/startbootstrap-sb-admin-2-gh-pages/data/roasterdata.js", "w") as output:
        out = jsTemplate.replace("$DATA", str(temperatures))
        out = out.replace("$BEANDATA", str(beantemps))
        output.write(out)
        output.flush()

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
