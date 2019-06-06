# encoding=utf8
from base_module import BaseModule as BaseModule
import macro_define as MD

class CommentModule(BaseModule):
    def __init__(self):
        super(CommentModule, self).__init__()
        self.module_name = ""

    def init(self):
        """
         comment_id:     评论主键
         comment_people: 上传者名字
         comment_time:   评论时间
         comment_course: 评论课程
         comment_text:   评论内容
        """
        self.module_name = "remy_course_comments"
        create_sql = 'CREATE TABLE IF NOT EXISTS %s       \
                (comment_id int NOT NULL AUTO_INCREMENT,  \
                comment_people varchar(50) NOT NULL,      \
                comment_time datetime NOT NULL,           \
                comment_course varchar(50) NOT NULL,      \
                comment_text text NOT NULL,               \
                PRIMARY KEY(comment_id))   \
                ENGINE=InnoDB DEFAULT charset=utf8        \
                '
        self.create_module(self.module_name, create_sql)

    def comment_add(self, course_name, comment_people, comment_text):
            add_sql = "INSERT INTO %s(comment_people, comment_course, comment_time, comment_text) VALUES('%s', '%s', now(), '%s')"

            self.cursor.execute(add_sql % (self.module_name, comment_people, course_name, comment_text))
            self.conn.commit()
            return {"msg":"添加成功！"}





















