# encoding=utf8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from tornado.web import RequestHandler as RequestHandler 
import tornado.gen as gen
sys.path.append("../")
import macro_define as MD

dir_map={
"1":"static/course_meta",
"2":"static/course_pic",
}

class FileHandler(RequestHandler):
    
    def video_upload(self):

        main_dir = "static/course_meta"
        snd_level_dir = self.get_argument("course_name", "");
        file_name = self.get_argument("chapter_name", "")+".mp4";

        request_file = self.request.files["chapter_file"][0]

        dir_name = os.path.join(MD.ROOT_PATH, main_dir + '/' + snd_level_dir)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        file_path = os.path.join(dir_name, file_name)
        with open(file_path, "wb") as file_meta:
            try:
                file_meta.write(request_file["body"])
            except Exception as e:
                self.write(str(e));
                return
        self.write("上传成功！")

    def pic_upload(self):

        main_dir = "static/course_pic"
        file_name = self.get_argument("course_name")

        request_file = self.request.files["course_file"][0]
        request_file_name = request_file["filename"]
        # 获取文件后缀
        if request_file_name.find('.') != -1:
            file_suffix = request_file_name.split('.')[1]

        dir_name = os.path.join(MD.ROOT_PATH, main_dir)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        file_path = os.path.join(dir_name, file_name + '.' + file_suffix)
        with open(file_path, "wb") as file_meta:
            try:
                file_meta.write(request_file["body"])
            except Exception as e:
                self.write(str(e));
                return
        self.write("上传成功！")

    @gen.coroutine
    def post(self):
        
        file_type = int(self.get_argument("file_type", "0"))
        if file_type == 1:
            self.video_upload()
        elif file_type == 2:
            self.pic_upload()
                  

        





































