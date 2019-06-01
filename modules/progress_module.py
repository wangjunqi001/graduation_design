# encoding=utf8
from base_module import BaseModule as BaseModule
import macro_define as MD

class ProgressModule(BaseModule):
    def __init__(self):
        super(ProgressModule, self).__init__()
        self.module_name = ""

    def init(self):
        """
        """
        self.module_name = "remy_course_progresses"
        create_sql = 'CREATE TABLE IF NOT EXISTS %s           \
                (course varchar(50) NOT NULL ,                \
                chapter varchar(50) NOT NULL ,                \
                student_name varchar(20) NOT NULL,            \
                state int(1) DEFAULT 0 NOT NULL,              \
                seq int(2) NOT NULL,                          \
                task text DEFAULT NULL,                       \
                teacher_comment text DEFAULT NULL,            \
                begin_time datetime NOT NULL,                 \
                end_time datetime NOT NULL,                   \
                PRIMARY KEY(course, chapter, student_name))   \
                ENGINE=InnoDB DEFAULT charset=utf8            \
                '
        self.create_module(self.module_name, create_sql)

    def progress_create(self, course_name, student_name, chapter_list):
        
        insert_sql = "INSERT INTO %s(course, chapter, student_name, seq, begin_time, end_time) VALUES('%s', '%s', '%s', %d, now(), now())"
        for i in range(len(chapter_list)):
            try:
                self.cursor.execute(insert_sql % (self.module_name, course_name, chapter_list[i], student_name, i))
            except Exception as e:
                return {"msg":str(e)}
            self.conn.commit()

        return {"msg":"添加成功！"}
            
        

























