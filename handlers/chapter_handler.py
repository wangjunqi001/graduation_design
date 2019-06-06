# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from tornado.web import RequestHandler as RequestHandler 
import tornado.gen as gen
sys.path.append("../")
from modules.chapter_module import ChapterModule as ChapterModule
from modules.progress_module import ProgressModule as ProgressModule

chapter_info_list = ["course_name", "chapter_name", "chapter_text", "chapter_task"]

class ChapterHandler(RequestHandler):

    def initialize(self):
        self.chapter_module = ChapterModule()
        self.chapter_module.init()
        self.progress_module = ProgressModule()
        self.progress_module.init()

    def chapter_add(self):

        ret = {}
        chapter_dict = {x:(self.get_argument(x, default="").decode("utf8")) for x in chapter_info_list}
        is_last_chapter = int(self.get_argument("is_last_chapter", "0"))

        teacher_name = self.get_cookie("name")
        try:
            ret = self.chapter_module.chapter_add(chapter_dict)
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

    def progress_create(self):

        course_name = self.get_argument("course_name").decode("utf8")
        student_name = self.get_cookie("name")
        table_name = "remy_course_courses"
        field_content = "chapter_list, student_list"
        condition = "course_name='%s'" % course_name 
        chapter_list = self.chapter_module.select(table_name, field_content, condition)[0][0]
        student_list = self.chapter_module.select(table_name, field_content, condition)[0][1]
        chapter_list = chapter_list.split("-")

        try:
            ret = self.progress_module.progress_create(course_name, student_name, chapter_list)
        except Exception as e:
            self.write("<h2>chapter_module_error: %s</h2>" % str(e))
            return 
            
        table_name = "remy_course_courses"
        if student_list != None and student_list != "":
            student_list += "-%s" % student_name 
        else:
            student_list = student_name 
        update_expr = "student_list='%s'" % student_list
        condition = "course_name='%s'" % course_name
        self.chapter_module.update(table_name, update_expr, condition)

        self.write(ret.get("msg"))

    def progress_query(self):

        course_map = {}

        student_name = self.get_cookie('name');
        table_name = self.progress_module.module_name
        field_content = "distinct course"
        condition = "student_name='%s'" % student_name
        course_list = self.progress_module.select(table_name, field_content, condition) 
        for course in course_list:
            course_map[course[0]] = {}
            field_content = "seq, chapter, state, end_time"
            condition = "student_name='%s' and course='%s' order by seq" % (student_name, course[0])
            chapter_list = self.progress_module.select(table_name, field_content, condition) 
            course_map[course[0]]["chapters"] = chapter_list

            pass_count = 0
            for chapter in chapter_list:
                if chapter[2] == 3:
                    pass_count += 1
            if pass_count == len(chapter_list):
                course_map[course[0]]["progress"] = 100
            else:
                progress = int(round(float(pass_count)/len(chapter_list), 2) * 100)
                course_map[course[0]]["progress"] = progress

        self.render("course-collection-list.html", COURSE_MAP=course_map)

    def task_query(self):

        course_map = {}

        teacher_name = self.get_cookie('name');
        table_name = "remy_course_courses"
        field_content = "course_name"
        # 教师关闭课程后将不在该教师的列表中显示该课程
        condition = "teacher_name='%s' and state=1" % teacher_name
        course_list = self.chapter_module.select(table_name, field_content, condition) 
        for course in course_list:
            course_map[course[0]] = []
            table_name = self.progress_module.module_name
            field_content = "end_time, chapter, student_name"
            condition = "course='%s' AND state=1 ORDER BY end_time" % course[0]
            task_list = self.progress_module.select(table_name, field_content, condition) 
            course_map[course[0]] = task_list
            
        self.render("course-task-list.html", COURSE_MAP=course_map)

    def task_comment(self):
        
        course_name = self.get_argument("course_name").decode("utf8")
        chapter_name = self.get_argument("chapter_name").decode("utf8")
        student_name = self.get_argument("student_name").decode("utf8")

        table_name = self.progress_module.module_name
        field_content = "task"
        condition = "student_name='%s' and course='%s' and chapter='%s'" % (student_name, course_name, chapter_name)
        task = self.progress_module.select(table_name, field_content, condition)[0][0] 

        table_name = self.chapter_module.module_name
        field_content = "chapter_task"
        condition = "course_name='%s' and chapter_name='%s'" % (course_name, chapter_name)
        task_desc = self.chapter_module.select(table_name, field_content, condition)[0][0] 

        self.render("task-comment.html", STUDENT_NAME=student_name,
        CHAPTER_NAME=chapter_name, COURSE_NAME=course_name,
        TASK=task, TASK_DESC=task_desc)

    def course_study(self):

        course_name = self.get_argument("course_name").decode("utf8")
        chapter_name = self.get_argument("chapter_name").decode("utf8")
        student_name = self.get_cookie("name")

        table_name = self.chapter_module.module_name
        field_content = "chapter_text, chapter_task"
        condition = "course_name='%s' and chapter_name='%s'" % (course_name, chapter_name)
        chapter_info = self.progress_module.select(table_name, field_content, condition)[0] 
        
        table_name = self.progress_module.module_name
        field_content = "state, task, teacher_comment"
        condition = "course='%s' and chapter='%s' and student_name='%s'" % (course_name, chapter_name, student_name)
        student_info = self.chapter_module.select(table_name, field_content, condition)[0] 
        
        field_content = "student_name, end_time, task, teacher_comment"
        condition = "course='%s' and chapter='%s' and state=3" % (course_name, chapter_name)
        task_list = self.chapter_module.select(table_name, field_content, condition)

        self.render("course-study.html", COURSE_NAME=course_name, \
        CHAPTER_NAME=chapter_name, CHAPTER_DESC=chapter_info[0], \
        CHAPTER_TASK=chapter_info[1], STATE=student_info[0], \
        TASK=student_info[1], TEACHER_COMMENT=student_info[2], \
        TASK_LIST=task_list)

    def task_comment_post(self):

        course_name = self.get_argument("course_name").decode("utf8")
        student_name = self.get_argument("student_name").decode("utf8")
        chapter_name = self.get_argument("chapter_name").decode("utf8")
        comment = self.get_argument("comment").decode("utf8")
        is_pass = self.get_argument("is_pass")

        table_name = self.progress_module.module_name
        update_expr = "state=%s, teacher_comment='%s', end_time=now()" % (is_pass, comment)
        condition = "course='%s' AND chapter='%s' AND student_name='%s'" % (course_name, chapter_name, student_name)
        try:
            self.chapter_module.update(table_name, update_expr, condition)
        except Exception as e:
            self.write(str(e))
            return

        self.write("作业处理成功！")

    def task_post(self):

        course_name = self.get_argument("course_name").decode("utf8")
        chapter_name = self.get_argument("chapter_name").decode("utf8")
        task = self.get_argument("task").decode("utf8")
        student_name = self.get_cookie("name")

        table_name = self.progress_module.module_name
        update_expr = "state=1, task='%s', end_time=now()" % task
        condition = "course='%s' AND chapter='%s' AND student_name='%s'" % (course_name, chapter_name, student_name)
        try:
            self.chapter_module.update(table_name, update_expr, condition)
        except Exception as e:
            self.write(str(e))
            return

        self.write("作业提交成功！")
        
        
    @gen.coroutine
    def get(self):
        op_type = int(self.get_argument("op_type", default="0"))
        if op_type == 1: # 进度表查询
            self.progress_query()
        elif op_type == 2: # 课程学习
            self.course_study()
        elif op_type == 3: # 教师查询已提交作业
            self.task_query()
        elif op_type == 4: # 教师作业评论
            self.task_comment()

    @gen.coroutine
    def post(self):
        
        op_type = int(self.get_argument("op_type", default="0"))
        if op_type == 1:   # 章节添加 
            self.chapter_add()
        elif op_type == 2: # 进度创建
            self.progress_create()
        elif op_type == 3: # 作业提交
            self.task_post()
        elif op_type == 4: # 作业提交
            self.task_comment_post()
        





























