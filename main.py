import time, roasterio, roasterhttpd

roast = roasterio.Roast("Guatemalan", "Full City Roast", 425)
roaster = roasterio.Roaster()

specFile = "roaster.spec"

with open(specFile, 'w') as content_file:
    content_file.write(str({'heater': 0, 'isRunning': 1, 'light': 10, 'scrollfan': 0, 'drum': 0, 'drawfan': 0}))
    content_file.flush()


httpd = roasterhttpd.ApiServer(roast, specFile)
httpd.start()

roaster.roastIt(roast, specFile)

while roaster.isRoasting:
    time.sleep(1)

roaster.exit()
httpd.stop()

print "roaster done"
