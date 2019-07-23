# __init__.py
import tornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
import json

define('port', default=8888, help='port to listen on')
define('ip', default="0.0.0.0", help='ip to listen on')


class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!!!!!!")

class InfoView(tornado.web.RequestHandler):
    """Only allow GET requests."""
    SUPPORTED_METHODS = ["GET"]

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def get(self):
        """List of routes for this API."""
        routes = {
            'info': 'GET /api/v1',
            'register': 'POST /api/v1/accounts',
            'single profile detail': 'GET /api/v1/accounts/<username>',
            'edit profile': 'PUT /api/v1/accounts/<username>',
            'delete profile': 'DELETE /api/v1/accounts/<username>',
            'login': 'POST /api/v1/accounts/login',
            'logout': 'GET /api/v1/accounts/logout',
            "user's tasks": 'GET /api/v1/accounts/<username>/tasks',
            "create task": 'POST /api/v1/accounts/<username>/tasks',
            "task detail": 'GET /api/v1/accounts/<username>/tasks/<id>',
            "task update": 'PUT /api/v1/accounts/<username>/tasks/<id>',
            "delete task": 'DELETE /api/v1/accounts/<username>/tasks/<id>'
        }
        self.write(json.dumps(routes))

def main():
    """Construct and serve the tornado application."""
    app = Application([
        (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": ""}),
        ('/', basicRequestHandler),
        ('/json', InfoView)
    ])
    http_server = HTTPServer(app)
    http_server.listen(options.port, options.ip)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()

if __name__=="__main__":
    main()