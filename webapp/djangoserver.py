import django, os
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
import BaseHTTPServer

isRunning = True

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        global isRunning
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        isRunning = False
        httpd.server_close()


def seed_data():
    from roasts.models import Roast, Bean, RoastLevel, Customer

    expectedRoastLevels = ["Cinnamon", "New England", "American", "City", "Full City", "Vienna", "French", "Italian", "Spanish"]
    roastLevels = RoastLevel.objects.all()

    if len(roastLevels) != len(expectedRoastLevels):
        for rl in expectedRoastLevels:
            roastLevel = RoastLevel(name=rl)
            roastLevel.save()

    expectedBeans = ["Guatemala Antigua Iglesias", "Indonesia Sulawesi"]
    beans = Bean.objects.all()

    if len(expectedBeans) != len(beans):
        for b in expectedBeans:
            bean = Bean(name=b)
            bean.save()

        c = Customer(name="House")
        c.save()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roasterui.settings")
    django.setup()
    application = get_wsgi_application()

    seed_data()
    call_command('runserver',  '127.0.0.1:8000')
