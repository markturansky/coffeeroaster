import time, roasterio, api

roast = roasterio.Roast("Guatemalan", "Full City Roast", 425)
roaster = roasterio.Roaster()

api = api.ApiServer(roast)
api.start()

roaster.roastIt(roast)

while roaster.isRoasting:
    time.sleep(1)

roaster.exit()
api.stop()

print "roaster done"
