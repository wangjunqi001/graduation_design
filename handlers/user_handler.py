# encoding=utf8
import sys

from tornado.web import RequestHandler as RequestHandler 
import tornado.gen as gen
sys.path.append("../")
from modules.user_module import UserModule as UserModule

user_info_list = ["name", "pass_wd", "user_type", "submit_type"]
user_type = ["学生账号", "教师账号"]

class UserHandler(RequestHandler):

    def __init__():
        super(UserHandler, self).__init__()
        self.user_dict = {}
        self.user_module = UserModule()
        self.user_module.init()

    @gen.coroutine
    def post():
        
        self.user_dict = {x:self.get_argument(x, default="") for x in user_info_list}

        try:
            ret = self.user_module.handler_user(self.user_dict)
        except Exception as e:
            self.write("user_module_error: %s", str(e))
        
        if ret.get("name", "") and ret.get("pass_wd", ""):
            self.render("user_ret.html", msg=("".join([user_type[ret["user_type"]], ret["msg"], " ", "用户名：", ret["name"]])))
        else:
            #TODO differnt format
            self.render("user_ret.html", msg=ret["msg"])
            
        
