import socketserver


class ClusterServer():

    def __init__(self, host="localhost", port=8787):
        self.host = host
        self.port = port
        socketserver.TCPServer.allow_reuse_address = True
        self.handler = lambda a, b, c: _ClusterServerHandler(a, b, c, cs=self)
        self.httpd = socketserver.TCPServer((host, port), self.handler)

    def serve_forever(self):
        self.httpd.serve_forever()

    def shutdown(self):
        self.httpd.shutdown()


class _ClusterServerHandler(socketserver.StreamRequestHandler):

    def __init__(self, a, b, c, cs):
        self.cs = cs
        socketserver.StreamRequestHandler.__init__(self, a, b, c)

    def handle(self):
        self.data = self.rfile.readline().strip()
        self.wfile.write(bytes("HTTP/1.1 200 OK\n\nASDASDASDASDF", "UTF-8"))
