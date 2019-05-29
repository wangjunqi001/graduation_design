# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from tornado.web import RequestHandler as RequestHandler 
import tornado.gen as gen
sys.path.append("../")
from modules.course_module import CourseModule as CourseModule

course_info_list = ["course_name", "chapter_list", "course_topic", "course_text"]

class CourseHandler(RequestHandler):

    def initialize(self):
        self.course_module = CourseModule()
        self.course_module.init()
        self.course_method = self.register_course_method()

    def register_course_method(self):
        return [
          self.course_module.course_add
        ]

    @gen.coroutine
    def get(self):
        
        

    @gen.coroutine
    def post(self):
        
        ret = {}
        course_dict = {x:(self.get_argument(x, default="").decode("utf8")) for x in course_info_list}
        course_dict["teacher_name"] = self.get_cookie("name").decode("utf8")
        
        op_type = int(self.get_argument("op_type", default="0"))
        if op_type > 0:
            try:
                ret = self.course_method[op_type - 1](course_dict)
            except Exception as e:
                self.write("<h2>course_module_error: %s</h2>" % str(e))

        chapter_list = course_dict.get("chapter_list", "").split('-') 

        if ret.get("msg") == "添加成功！":
            self.render("chapter-upload.html", CHAPTER_LIST=chapter_list, COURSE_NAME=course_dict.get("course_name"))
        else:
            self.write("<h2"+ ret.get("msg")+"</h2>");
            






















