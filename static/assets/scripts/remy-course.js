function addChapter() {
  var chapter_group = document.getElementById("chapter-group");
  var new_chapter = document.createElement("div");
  new_chapter.setAttribute("class", "form-element");
  var form_element = document.createElement("div");
  var label = document.createElement("div");
  label.setAttribute("class", "col-sm-1");
  form_element.setAttribute("class", "col-lg-3");
  new_chapter.appendChild(label);
  form_element.innerHTML =
    ' <input type="text" class="form-control" name="chapter_name" \
                                   placeholder="请输入章节名" autocomplete="off"/>';
  new_chapter.appendChild(form_element);
  chapter_group.appendChild(new_chapter);
}

function delChapter() {
  var chapter_group = document.getElementById("chapter-group");
  var last_chapter = chapter_group.lastChild;
  if (chapter_group.childNodes.length > 2) {
    chapter_group.removeChild(last_chapter);
  } else {
    var course_form = document.getElementById("course-form");
    var alert_box = document.createElement("div");
    var chapter_event = document.getElementById("chapter-event");
    alert_box.setAttribute("class", "alert alert-warning form-element");
    alert_box.style.height = "60px";
    alert_box.innerHTML =
      '<a href="#" class="close" data-dismiss="alert">&times;</a>至少需要一个章节';
    course_form.insertBefore(alert_box, chapter_event);
  }
}

function alertNone(target) {
  if (!target) {
    alert("输入为空哦， 检查一下吧！");
    return 0;
  }
  return 1;
}

// @function: ajax request & change main div content & post method
// @param1 url: request url
// @param2 url: request paramters     format: param1=value1&param2=value2
function ajaxPost(url, data) {
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST", url, true);
  xmlhttp.send(data);
  xmlhttp.onreadystatechange = function() {
    document.getElementById("main").innerHTML = xmlhttp.responseText;
  };
}

function createProgress(course_name){
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST", "/chapter", true);
	data = new FormData();
	data.append("op_type", "2");
	data.append("course_name", course_name);
	xmlhttp.send(data);

  xmlhttp.onreadystatechange = function() {
		alert(xmlhttp.responseText);
  };

	getStaticContent('/course');
}

function courseUpload() {
  var submit_confirm = confirm("准备好要提交了吗？");
  if (submit_confirm) {
    var course_name = document.getElementsByName("course_name");
    if (!alertNone(course_name[0].value)) return false;
    var chapter_names = document.getElementsByName("chapter_name");
    var course_topic = document.getElementById("course_topic");
		var index = course_topic.selectedIndex;
		var course_text = document.getElementById("course_text");
    var chapter_list = "";
    for (var i = 0; i < chapter_names.length; ++i) {
      if (!alertNone(chapter_names[i].value)) return false;
      if (i == 0) chapter_list += chapter_names[i].value;
      else chapter_list += "-" + chapter_names[i].value;
    }
    // ajax 提交信息
    var request_url = "/course";
		data = new FormData()
		data.append("course_name", course_name[0].value);
		data.append("chapter_list", chapter_list);
		data.append("course_topic", course_topic.options[index].text);
		data.append("course_text", course_text.value);
		data.append("op_type", "1");
		console.log(data);
    ajaxPost(request_url, data);
  } else return false;
}

// @function: ajax request & change main div content & get method & no param
// @param1 url: request url
function getStaticContent(url) {
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", url, true);
  xmlhttp.send();
  xmlhttp.onreadystatechange = function() {
    document.getElementById("main").innerHTML = xmlhttp.responseText;
  };
}

function requestCourseByKey(){
	var key = document.getElementById("search-box").value;
	if(!alertNone(key)) return;
	getStaticContent("/course?op_type=2&key="+key);
}

function metaFileUpload(index, type) {
  var fileObj = document.getElementById("chapter-file"+"-"+index);
  if (!fileObj || !fileObj.value) {
    alert("请选择图片");
    return;
  }
  var formData = new FormData();
  formData.append("chapter_file", fileObj.files[0]);
  formData.append(
    "chapter_name",
    document.getElementById("chapter-name-"+index).value
  );
  formData.append(
    "course_name",
    document.getElementById("chapter-course-name-"+index).value
  );
  formData.append("file_type", type);
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST", "/file", true);
  xmlhttp.send(formData);
  xmlhttp.onreadystatechange = function() {
    alert(xmlhttp.responseText);
  };
}

function chapterUpload(index){
  var submit_confirm = confirm("准备好要提交了吗？");
	if(submit_confirm){
    var course_name = document.getElementById("chapter-course-name-"+index).value;
    var chapter_name = document.getElementById("chapter-name-"+index).value;
    var chapter_text = document.getElementById("chapter-text-"+index).value;
    var chapter_task = document.getElementById("chapter-task-"+index).value;
  	var fileObj = document.getElementById("chapter-file"+"-"+index);
		if((!course_name) || (!chapter_name) || (!chapter_text) || (!chapter_task) || (!fileObj)|| (!fileObj.value)){
			alert("输入不能为空哦！");
		}

		var ucl = document.getElementById("upload-chapter-list");
		var cfc = document.getElementById("chapter-form-content");
		var is_last_chapter = (ucl.childNodes.length == 3) ? 1 : 0; 

		var formdata = new FormData();
  	formdata.append("is_last_chapter", is_last_chapter);
  	formdata.append("course_name", course_name);
  	formdata.append("chapter_name", chapter_name);
  	formdata.append("chapter_text", chapter_text);
  	formdata.append("chapter_task", chapter_task);
  	formdata.append("op_type", 1);
  	var xmlhttp = new XMLHttpRequest();
  	xmlhttp.open("POST", "/chapter", true);
  	xmlhttp.send(formdata);
  	xmlhttp.onreadystatechange = function() {
			if(!is_last_chapter){
    		var resp = xmlhttp.responseText;
				if(resp=="上传成功"){ //删除上传成功的节点
					ucl.removeChild((ucl.childNodes)[2 * index + 1]);
					cfc.removeChild((cfc.childNodes)[2 * index + 1]);
				}	
				alert(resp);
			}
			else{
				document.body.innerHTML = xmlhttp.responseText;
				alert("上传成功！");
			}
  	};
	}else return false;
}












