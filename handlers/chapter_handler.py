# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from tornado.web import RequestHandler as RequestHandler 
import tornado.gen as gen
sys.path.append("../")
from modules.chapter_module import ChapterModule as ChapterModule

chapter_info_list = ["course_name", "chapter_name", "chapter_text", "chapter_task"]

class ChapterHandler(RequestHandler):

    def initialize(self):
        self.chapter_module = ChapterModule()
        self.chapter_module.init()
        self.chapter_method = self.register_chapter_method()

    def register_chapter_method(self):
        return [
          self.chapter_module.chapter_add
        ]

    @gen.coroutine
    def post(self):
        
        ret = {}
        chapter_dict = {x:(self.get_argument(x, default="").decode("utf8")) for x in chapter_info_list}
        is_last_chapter = int(self.get_argument("is_last_chapter", "0"))

        op_type = int(self.get_argument("op_type", default="0"))
        teacher_name = self.get_cookie("name")
        print chapter_dict
        if op_type > 0:
            try:
                ret = self.chapter_method[op_type - 1](chapter_dict)
            except Exception as e:
                self.write("<h2>chapter_module_error: %s</h2>" % str(e))

        if ret.get("msg") == "上传成功" and is_last_chapter:
            table_name = "remy_course_courses"
            update_expr = "state=1"
            condition = "teacher_name='" + teacher_name + "' and course_name='" + self.get_argument("course_name", default="").decode("utf8") + "'"   
            self.chapter_module.update(table_name, update_expr, condition)
            self.render("index.html", NAME=self.get_cookie("name"), USER_TYPE=1)
        else:
            self.write(ret.get("msg"));





























