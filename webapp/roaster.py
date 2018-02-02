import django, os
from django.core.wsgi import get_wsgi_application
import time, sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roasterui.settings")
    django.setup()
    application = get_wsgi_application()

    from roasts.roaster import Roaster
    roaster = Roaster()
    roaster.start()
    print "started roaster thread"

    while True:
        try:
            time.sleep(60)
        except KeyboardInterrupt:
            print "stopping roaster..."
            roaster.stop()
            time.sleep(2)
            print "Bye"
            sys.exit()
