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

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roasterui.settings")
    django.setup()
    application = get_wsgi_application()

    call_command('runserver',  '127.0.0.1:8000')
