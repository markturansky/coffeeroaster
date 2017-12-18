from BaseHTTPServer import HTTPServer
import SimpleHTTPServer, cgi, threading, time


# an evil global ...
roast = None

class S(SimpleHTTPServer.SimpleHTTPRequestHandler, object):
    def do_GET(self):
        if "rest" not in self.path:
            super(S, self).do_GET()
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        global roast

        envTemps = []
        beantemps = []
        counter = 0
        for r in roast.data:
            timestamp = r[0]
            bt = r[1]["beanTemp"]
            et = r[1]["envTemp"]
            envTemps.append([counter, et])
            beantemps.append([counter, bt])
            counter = counter + 1

        temperatures = [envTemps, beantemps]
        self.wfile.write(str(temperatures))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print post_data # <-- Print post data
        self._set_headers()


class ApiServer:
    def __init__(self, r):
        global roast
        roast = r

    def start(self):
        self.httpd = HTTPServer(('', 8888), S)
        self.thread = threading.Thread(name="Smart Roaster API Server", target=self.run)
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.httpd.shutdown()

    def run(self):
        while self.running:
            print 'Starting httpd...'
            self.httpd.serve_forever()
        print "exiting api server"

