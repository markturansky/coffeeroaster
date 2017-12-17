import time, sys, copy

import roaster, roast, roasterio

roaster = roaster.Roaster()
r = roast.Roast("Guatemalan", "Full City Roast", 425)

roastdata = []

started = time.time()

def run():
    isRunning = True
    while isRunning:
        # loop in 10s chunks of time
        for i in range(10):
            isRunning, specData = roasterio.refreshSpec("roaster.spec")

            if isRunning == False:
                return

            for key in specData:
                desiredValue = specData[key]
                roaster.setWhenDifferent(key, desiredValue)
            roaster.reconcile(i)

            snapshot = roaster.snapshot()
            r.add(snapshot)

            roasterio.saveGraphData(r.data)
            time.sleep(1)

run()
roaster.exit()
print "roaster done"
