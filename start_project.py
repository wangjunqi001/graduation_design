# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import tornado.ioloop
from tornado.web import RequestHandler as RequestHandler 
from tornado.web import Application as Application

from handlers.user_handler import UserHandler as UserHandler
from handlers.course_handler import CourseHandler as CourseHandler
from handlers.file_handler import FileHandler as FileHandler
from handlers.chapter_handler import ChapterHandler as ChapterHandler

class TestHandler(RequestHandler):
    def get(self):
        self.render("test.html", NAME="test")

class LoginHandler(RequestHandler):
    def get(self):
        self.render("page-login.html")

class UploadHandler(RequestHandler):
    def get(self):
        self.render("course-upload.html")

def init_app():
    return Application([
        # 动态网页
        (r"/user", UserHandler),
        (r"/course", CourseHandler),
        (r"/file", FileHandler),
        (r"/chapter", ChapterHandler),

        # 静态网页，为了能够使用asset以及ajax局部更新，也需要走模板，不走static
        # static的唯一作用就是提供js css img等素材支持
        (r"/test", TestHandler),
        (r"/login", LoginHandler),
        (r"/course_upload", UploadHandler)
    ],
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    debug = True 
    )

if __name__ == "__main__":
    app = init_app()
    app.listen(9696)
    tornado.ioloop.IOLoop.current().start()











