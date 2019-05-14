# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from tornado.web import RequestHandler as RequestHandler 
import tornado.gen as gen
sys.path.append("../")
from modules.user_module import UserModule as UserModule

user_info_list = ["name", "pass_wd", "user_type", "submit_type"]
user_type = ["学生账号", "教师账号"]

class UserHandler(RequestHandler):

    def initialize(self):
        self.user_dict = {}
        self.user_module = UserModule()
        self.user_module.init()

    @gen.coroutine
    def post(self):
        
        ret = {}
        ret_msg = ""

        self.user_dict = {x:self.get_argument(x, default="") for x in user_info_list}

        try:
            ret = self.user_module.handler_user(self.user_dict)
        except Exception as e:
            self.write("user_module_error: %s" % str(e))

        if ret.get("msg") == "登录成功！":
            ret_msg = "".join([user_type[int(ret["user_type"])], ret["msg"], " ", "用户名：", self.user_dict["name"]])
            self.set_cookie("name", unicode(self.user_dict["name"]))
            self.set_cookie("pass_wd", unicode(self.user_dict["pass_wd"]))
            self.set_cookie("user_type", unicode(ret["user_type"]))
            #TODO different user
            self.render("index.html", NAME=self.user_dict["name"])
        elif ret.get("msg") == "注册成功！":
            ret_msg = "".join([user_type[int(self.user_dict["user_type"])], ret["msg"], " ", "用户名：", self.user_dict["name"]])
            self.render("user_ret.html", msg=ret_msg, mark=1)
        elif ret.get("msg") == "注销成功！":
            self.set_cookie("name", "")
            self.set_cookie("pass_wd", "")
            self.set_cookie("user_type", "")
            self.render("page-login.html")
        else:
            self.render("user_ret.html", msg=ret["msg"], mark=0)
        
            
        
