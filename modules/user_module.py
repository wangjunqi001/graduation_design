# encoding=utf8
from base_module import BaseModule as BaseModule
import macro_define as MD

class UserModule(BaseModule):
    def __init__(self):
        super(user_module, self).__init__()
        self.module_name = ""

    def init(self):
        self.table_name = "easy_course_users"
        create_sql =  '''
        CREATE TABLE %s (
        name varchar(20),
        pass_wd varchar(15) NOT NULL,
        user_type ENUM(0,1,2) NOT NULL,
        PRIMARY KEY(name)
        CHECK (length(pass_wd)>=6)
        )engine=INNODB DEFAULT charset=utf8
        '''
        self.create_module(self.module_name, create_sql)

    def handler_user(self, user_info_dict):
        op_type = int(user_info_dict.get("submit_type", MD.USER_DEFAULT))
        
        if op_type == MD.USER_REGISTER:
            return self.user_register(self, user_info_dict)
        elif op_type == MD.USER_VERIFICATION:
            return self.user_verification(self, user_info_dict)
        else:
            return {"msg":"未定义的操作类型！"}

    def user_register(self, user_info_dict):
        ret_dict = {}
        name = user_info_dict.get("name", "")
        pass_wd = user_info_dict.get("name", "")
        user_type = int(user_info_dict.get("user_type", 0))
        # 密码不能为空，长度必须在[6, 15]区间之内
        if name == "" or pass_wd == "":
            ret_dict["msg"] = "用户名或密码不能为空！"
            return ret_dict
        elif len(pass_wd) < 6 or len(pass_wd) > 15:
            ret_dict["msg"] = "密码长度需在6~15之间！"
            return ret_dict

        select_name_sql = "SELECT name from %s where name='%s'" 

        select_ret = self.cursor.execute(select_name_sql % (self.module_name, name))
        if select_ret == 0:
            register_sql = "INSERT INTO %s(name, pass_wd, user_type) VALUES(%s, %s, %s)"
            try:
                self.cursor.execute(register_sql % (self.module_name, name, pass_wd, user_type))
            except Exception as e:
                ret_dict["msg"] = str(e)
                return ret_dict
            ret_dict["msg"] = "注册成功！"
            ret_dict["name"] = name
            ret_dict["pass_wd"] = pass_wd
            ret_dict["user_type"] = user_type
        else:
            ret_dict["msg"] = "用户名已存在！"
            return ret_dict 
        




















