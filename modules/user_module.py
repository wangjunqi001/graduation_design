import base_module.base_module as BaseModule
import macro_define as MD

class user_module(BaseModule):
    def __init__(self):
        super(user_module, self).__init__()

    def handler_user(self, user_info_dict):
        op_type = user_info_dict.get("submit_type", MD.USER_DEFAULT)
        
        if op_type = MD.USER_REGISTER:
            return self.user_register(self, user_info_dict)

        if op_type = MD.USER_VERIFICATION:
            return self.user_verification(self, user_info_dict)

        else
            return "未定义的操作类型"

