# encoding=utf8
from base_module import BaseModule as BaseModule
import macro_define as MD

class UserModule(BaseModule):
    def __init__(self):
        super(UserModule, self).__init__()
        self.module_name = ""

    def init(self):
        self.module_name = "remy_course_users"
        create_sql = 'CREATE TABLE IF NOT EXISTS %s  \
                (name varchar(20) PRIMARY KEY,       \
                pass_wd varchar(15) NOT NULL,        \
                user_type int(2) NOT NULL ,          \
                CHECK(length(pass_wd)>=6))           \
                ENGINE=InnoDB DEFAULT charset=utf8   \
                '
        self.create_module(self.module_name, create_sql)

    def has_user_name(self, user_name):
        select_name_sql = "SELECT name FROM %s WHERE name='%s'" 

        return self.cursor.execute(select_name_sql % (self.module_name, user_name))

    def handler_user(self, user_info_dict):
        op_type = int(user_info_dict.get("submit_type", MD.USER_DEFAULT))
        if op_type == MD.USER_REGISTER:
            return self.user_register(user_info_dict)
        elif op_type == MD.USER_VERIFICATION:
            return self.user_verification(user_info_dict)
        elif op_type == MD.USER_LOGOUT:
            return self.user_logout()
        else:
            return {"msg":"未定义的操作类型！"}

    def user_register(self, user_info_dict):

        name = str(user_info_dict.get("name", ""))
        pass_wd = str(user_info_dict.get("pass_wd", ""))
        user_type = int(user_info_dict.get("user_type", "0"))
        # 密码不能为空，长度必须在[6, 15]区间之内
        if name == "" or pass_wd == "":
            return {"msg":"用户名或密码不能为空！"}
        elif len(pass_wd) < 6 or len(pass_wd) > 15:
            return {"msg":"密码长度需在6~15之间！"}

        if self.has_user_name(name) == 0:
            register_sql = "INSERT INTO %s(name, pass_wd, user_type) VALUES('%s', '%s', %s)"
            try:
                self.cursor.execute(register_sql % (self.module_name, name, pass_wd, user_type))
            except Exception as e:
                return  str(e)
            self.conn.commit()
            return {"msg":"注册成功！"}
        else:
            return {"msg":"用户名已存在！"}

    def user_verification(self, user_info_dict):

        ret_dict = {}

        name = str(user_info_dict.get("name", ""))
        pass_wd = str(user_info_dict.get("pass_wd", ""))
    
        if name == "" or pass_wd == "":
            return {"msg":"请输入用户名或密码！"}
        elif self.has_user_name(name) == 1:
            verification_sql = "SELECT pass_wd,user_type FROM %s WHERE name='%s'"
            try:
                self.cursor.execute(verification_sql % (self.module_name, name))
                result = self.cursor.fetchone()
                db_pass_wd = str(result[0])
                user_type = int(result[1])
                if db_pass_wd == pass_wd:
                    ret_dict["msg"] = "登录成功！"
                    ret_dict["user_type"] = user_type
                    return ret_dict
                else:
                    return {"msg":"用户名或密码错误！"}
            except Exception as e:
                return  {"msg":str(e)}
        else:
            return {"msg":"用户名不存在！"}
            
    def user_logout(self):
        return {"msg":"注销成功！"}
        




















