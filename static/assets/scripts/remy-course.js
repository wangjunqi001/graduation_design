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
      '<a href="#" class="close" data-dismiss="alert">&times;</a>\
                                 至少需要一个章节';
    course_form.insertBefore(alert_box, chapter_event);
  }
}

function alertNone(target) {
  if (!target) {
    alert("有输入为空的表单哦， 检查一下吧！");
    return 0;
  }
  return 1;
}

function courseUpload() {
  var submit_confirm = confirm("准备好要提交了吗？");
  if (submit_confirm) {
    var course_name = document.getElementsByName("course_name");
    if (!alertNone(course_name[0].value)) return false;
    var chapter_names = document.getElementsByName("chapter_name");
    var chapter_list = "";
    for (var i = 0; i < chapter_names.length; ++i) {
      if (!alertNone(chapter_names[i].value)) return false;
      if (i == 0) chapter_list += chapter_names[i].value;
      else chapter_list += "#" + chapter_names[i].value;
    }
    // ajax 提交信息
    var course_info = course_namaxe[0].value;
    document.write(chapter_list);
  } else return false;
}

// @function: ajax request & change main div content & get method & no param
// @param1 url: request url
// @param2 method: request method
// @param3 params: request parameters
function getStaticContent(url) {
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", url, true);
  xmlhttp.send();
  xmlhttp.onreadystatechange = function() {
    document.getElementById("main").innerHTML = xmlhttp.responseText;
  };
}
