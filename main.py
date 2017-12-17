import time, roasterio

roast = roasterio.Roast("Guatemalan", "Full City Roast", 425)
roaster = roasterio.Roaster()

roaster.roastIt(roast)

while roaster.isRoasting:
    time.sleep(1)

roaster.exit()
print "roaster done"
