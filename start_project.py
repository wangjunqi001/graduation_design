import os
import tornado.ioloop
from tornado.web import RequestHandler as RequestHandler 
from tornado.web import Application as Application

from handlers.user_handler import UserHandler as UserHandler

class TestHandler(RequestHandler):
    def get(self):
        self.render("test.html", NAME="test")

class LoginHandler(RequestHandler):
    def get(self):
        self.render("page-login.html")

def init_app():
    return Application([
        (r"/user", UserHandler),
        (r"/test", TestHandler),
        (r"/login", LoginHandler)
    ],
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    debug = True
    )

if __name__ == "__main__":
    app = init_app()
    app.listen(9696)
    tornado.ioloop.IOLoop.current().start()











