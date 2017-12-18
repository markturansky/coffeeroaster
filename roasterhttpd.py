from BaseHTTPServer import HTTPServer
import urlparse
import SimpleHTTPServer, cgi, threading, time


# evil globals ...
roast = None
spec = None

class S(SimpleHTTPServer.SimpleHTTPRequestHandler, object):
    def do_GET(self):
        global roast, spec

        # anything not /rest is normal web serving
        if "rest" not in self.path:
            super(S, self).do_GET()
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # anything not /rest/set is basic getter of current roaster data
        if "set" not in self.path:
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
            return

        parsed = urlparse.urlparse(self.path)
        params = urlparse.parse_qs(parsed.query)

        with open(spec, 'r') as content_file:
            specdata = content_file.read()
            specdata = eval(specdata)

        for key in params:
            if specdata.has_key(key):
                value = params[key][0]
                specdata[key] = int(value)

        with open(spec, 'w') as content_file:
            content_file.write(str(specdata))
            content_file.flush()
        self.wfile.write(str(specdata))

    # def do_HEAD(self):
    #     self._set_headers()

class ApiServer:
    def __init__(self, r, f):
        global roast, spec
        roast = r
        spec = f


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
