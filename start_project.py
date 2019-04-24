import os
import tornado.ioloop
import tornado.web.RequestHandler as RequestHandler 
import tornado.web.Application as Application

from handlers.user_handler import UserHandler

class MainHandler(RequestHandler):
    def get(self):
        self.render("demo.html", msg = "666,play with tornado")

def init_app():
    return Application([
        (r"/remy", MainHandler),
        (r"/user", UserHandler)
    ],
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    debug = True
    )

if __name__ == "__main__":
    app = init_app()
    app.listen(9696)
    tornado.ioloop.IOLoop.current().start()
