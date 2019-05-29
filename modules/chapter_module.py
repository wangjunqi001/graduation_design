# encoding=utf8
from base_module import BaseModule as BaseModule
import macro_define as MD

class ChapterModule(BaseModule):
    def __init__(self):
        super(ChapterModule, self).__init__()
        self.module_name = ""

    def init(self):
        """
         course_name: 课程标题
         chapter_name: 上传者名字
         chapter_task: 任务描述
         chapter_text: 章节内容描述
        """
        self.module_name = "remy_course_chapters"
        create_sql = 'CREATE TABLE IF NOT EXISTS %s       \
                (course_name varchar(50) NOT NULL, \
                chapter_name varchar(50) NOT NULL, \
                chapter_text text NOT NULL,               \
                chapter_task text NOT NULL,               \
                PRIMARY KEY(course_name, chapter_name))   \
                ENGINE=InnoDB DEFAULT charset=utf8        \
                '
        self.create_module(self.module_name, create_sql)

    def chapter_add(self, chapter_dict):
        course_name = chapter_dict.get("course_name", "")
        chapter_name = chapter_dict.get("chapter_name", "")
        chapter_text = chapter_dict.get("chapter_text", "")
        chapter_task = chapter_dict.get("chapter_task", "")
        
        add_sql = "INSERT INTO %s(course_name, chapter_name, chapter_text, chapter_task) VALUES('%s', '%s', '%s', '%s')"
        try:
            self.cursor.execute(add_sql % (self.module_name, course_name, chapter_name, chapter_text, chapter_task))
        except Exception as e:
            return {"msg":str(e)}
        self.conn.commit()
        return {"msg":"上传成功"}











