# encoding=utf8
import sys
import random
reload(sys)
sys.setdefaultencoding('utf8')
from tornado.web import RequestHandler as RequestHandler 
import tornado.gen as gen
sys.path.append("../")
from modules.course_module import CourseModule as CourseModule
from modules.comment_module import CommentModule as CommentModule

course_info_list = ["course_name", "chapter_list", "course_topic", "course_text"]

class CourseHandler(RequestHandler):

    def initialize(self):
        self.course_module = CourseModule()
        self.comment_module = CommentModule()
        self.course_module.init()
        self.comment_module.init()

    def render_course_preview(self, course_name):
        table_name = "remy_course_courses"
        field_content = "teacher_name, course_desc, chapter_list, student_list"
        condition = "course_name='%s' AND state=1" % course_name
        course_info = self.course_module.select(table_name, field_content, condition)[0]
        chapter_list = course_info[2].split("-")
        has_collected = False
        student_list = []
        if course_info[3] != None and course_info[3] != "":
            student_list = course_info[3].split("-")
        if self.get_cookie("name") in student_list:
            has_collected = True
        table_name = "remy_course_comments"
        field_content = "comment_people, comment_time, comment_text"
        condition = "comment_course='%s'" % course_name
        comment_list = self.comment_module.select(table_name, field_content, condition)

        self.render("course-preview.html", COURSE_NAME=course_name,\
        COURSE_TEXT=course_info[1], CHAPTER_LIST=chapter_list, \
        TEACHER_NAME=course_info[0], STUDENT_LIST=student_list, \
        COMMENT_LIST=comment_list, HAS_COLLECTED=has_collected)

    def render_index(self):
        table_name = "remy_course_courses"
        field_content = "course_name"
        condition = "state=1"
        course_list = list(self.course_module.select(table_name, field_content, condition))
        random.shuffle(course_list)
        self.render("real-index.html", COURSE_LIST=course_list)
            
    def render_state_manage(self):
        course_map = []
        teacher = self.get_cookie("name", default="").decode("utf8")    
        
        table_name = "remy_course_courses"
        field_content = "course_name, state, student_list"
        condition = "teacher_name='%s'" % teacher
        course_list = self.course_module.select(table_name, field_content, condition)
        for course in course_list:
            course_info = {}
            course_name = course[0].encode('utf-8')
            course_info["name"] = course_name
            course_info["state"] = course[1]
            course_info["progresses"] = {}
            student_list = []
            if course[2] != "":
                student_list = course[2].split("-")
            for student in student_list:
                student_name = student.encode('utf-8')
                table_name = "remy_course_progresses"
                field_content = "state"
                condition = "course='%s' and student_name='%s'" % (course_name, student_name)
                state_list = self.course_module.select(table_name, field_content, condition)
                pass_count = 0
                for state in state_list:
                    if state[0] == 3:
                        pass_count += 1
                if len(state_list) != 0:
                    course_info["progresses"][student_name] = int(round(float(pass_count)/len(state_list), 2) * 100)
                else:
                    course_info["progresses"][student_name] = 0
            course_map.append(course_info)

        self.render("course-manage.html", COURSE_MAP=course_map)

    @gen.coroutine
    def get(self):
        course_name = self.get_argument("course_name", default="").decode("utf8")    
        if course_name != "":
            self.render_course_preview(course_name)
            return
        op_type=int(self.get_argument("op_type",default="0"))    
        table_name = "remy_course_courses"
        field_content = "course_name, course_topic, teacher_name"
        condition = "state=1"
        if op_type == 1:
            topic = self.get_argument("topic", default="")
            condition += " and course_topic = '%s'" % topic
        elif op_type == 2:
            key = self.get_argument("key", default="")   
            condition += " and (course_name LIKE '%%%s%%' OR chapter_list LIKE '%%%s%%' OR teacher_name LIKE '%%%s%%' OR course_desc LIKE '%%%s%%')" % (key, key, key, key)
        elif op_type == 3:
            self.render_index()
            return
        elif op_type == 4:
            self.render_state_manage()
            return
        course_list = self.course_module.select(table_name, field_content, condition)
        self.render("course-search.html", COURSE_LIST=course_list)

    def comment_add(self):

        ret = {}
        course_name = self.get_argument("course_name", default="").decode("utf8")    
        comment_people = self.get_cookie("name", default="").decode("utf8")    
        comment_text = self.get_argument("comment_text", default="").decode("utf8")    
        
        try:
            ret = self.comment_module.comment_add(course_name, comment_people, comment_text)
        except Exception as e:
            self.write("<h2>comment_module_error: %s</h2>" % str(e))

        self.write("<h2>"+ ret.get("msg")+"</h2>");
        
    def course_add(self):

        ret = {}
        course_dict = {x:(self.get_argument(x, default="").decode("utf8")) for x in course_info_list}
        course_dict["teacher_name"] = self.get_cookie("name").decode("utf8")
        
        try:
            ret = self.course_module.course_add(course_dict)
        except Exception as e:
            self.write("<h2>course_module_error: %s</h2>" % str(e))

        chapter_list = course_dict.get("chapter_list", "").split('-') 

        if ret.get("msg") == "添加成功！":
            self.render("chapter-upload.html", CHAPTER_LIST=chapter_list, COURSE_NAME=course_dict.get("course_name"))
        else:
            self.write("<h2"+ ret.get("msg")+"</h2>");

    def modify_course_state(self):
        
        course_name = self.get_argument("course_name", default="").decode("utf8")    
        state = self.get_argument("state", default="") 

        table_name = "remy_course_courses"
        update_expr = "state=%s" % state
        condition = "course_name='%s'" % course_name
        self.course_module.update(table_name, update_expr, condition)

        self.write("操作成功！")

    @gen.coroutine
    def post(self):
        
        op_type = int(self.get_argument("op_type", default="0"))
        if op_type == 1:   # 课程创建
            self.course_add()
        elif op_type == 2: # 评论添加
            self.comment_add()
        elif op_type == 3: # 课程状态修改
            self.modify_course_state()
            






















