# encoding=utf8
import sys

import tornado.web.RequestHandler as RequestHandler 
import tornado.gen as gen
sys.path.append("../")
import modules.user_module.user_module as UserModule

user_info_list = ["name", "pass_wd", "user_type", "submit_type"]

class UserHandler(RequestHandler):

    def __init__():
        super(UserHandler, self).__init__()
        self.user_dict = {}

    @gen.coroutine
    def post():
        
        self.user_dict = {x:self.get_argument(x, default="") for x in user_info_list}

        try:
            ret = UserModule.handler_user(self.user_dict)
        except Exception as e:
            self.write("user_module_error: %s", str(e))
        
        # 用户反馈信息
        self.render("user_ret.html", msg=ret)
            
        
