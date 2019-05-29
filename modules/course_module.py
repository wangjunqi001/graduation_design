# encoding=utf8
from base_module import BaseModule as BaseModule
import macro_define as MD

class CourseModule(BaseModule):
    def __init__(self):
        super(CourseModule, self).__init__()
        self.module_name = ""

    def init(self):
        """
         course_name: 课程标题
         course_topic: 课程主题
         course_desc: 课程描述
         teacher_name: 上传者名字
         chapter_list: 章节列表 每个章节使用#分隔
         student_list: 学生列表 每个学生使用#分隔
         state: 1 打开 0 关闭 2 未完成上传
        """
        self.module_name = "remy_course_courses"
        create_sql = 'CREATE TABLE IF NOT EXISTS %s       \
                (course_name varchar(50) NOT NULL,        \
                course_topic varchar(50) NOT NULL,        \
                teacher_name varchar(20) NOT NULL,        \
                chapter_list TEXT DEFAULT NULL,           \
                course_desc  TEXT DEFAULT NULL,           \
                student_list TEXT DEFAULT NULL,           \
                state int(1) DEFAULT 2,                   \
                PRIMARY KEY(course_name, teacher_name))   \
                ENGINE=InnoDB DEFAULT charset=utf8        \
                '
        self.create_module(self.module_name, create_sql)

    def has_dup_course(self, teacher_name, course_name):
        select_sql = "SELECT course_name, teacher_name FROM %s WHERE teacher_name='%s' and course_name='%s' " 
        return self.cursor.execute(select_sql % (self.module_name, teacher_name, course_name))

    def course_add(self, course_dict):
        teacher_name = course_dict.get("teacher_name", "")
        course_name = course_dict.get("course_name", "")
        chapter_list = course_dict.get("chapter_list", "")
        course_desc = course_dict.get("course_text", "")
        course_topic = course_dict.get("course_topic", "")

        if self.has_dup_course(teacher_name, course_name) == 0:
            add_sql = "INSERT INTO %s(course_name, teacher_name, chapter_list, course_desc, course_topic) VALUES('%s', '%s', '%s', '%s', '%s')"
            try:
                self.cursor.execute(add_sql % (self.module_name, course_name, teacher_name, chapter_list, course_desc, course_topic))
            except Exception as e:
                raise e
            self.conn.commit()
            return {"msg":"添加成功！", "chapter_list":chapter_list}
        else:
            return {"msg":"同一教师无法上传同名课程！"}

        






























