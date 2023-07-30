userInfo = null
is_admin = false
userId = ''
setUserInfo()

function setUserInfo() {
    if (null != localStorage.userInfo){
        userInfo = JSON.parse(localStorage.userInfo);
        if(null != userInfo){
            $("#userName").text(userInfo.user_name);
            userId = userInfo.id;
            localStorage.userId = userId
            is_admin = userInfo.is_admin
        }else{
            setTimeout(function() {
                window.location.href='/static/page/login-1.html';
              },1500); 
        }
        
    }else{
        setTimeout(function() {
          window.location.href='/static/page/login-1.html';
        },1500);
    }
}

function successMsg(msg) {
    var content = "";
    if (isEmpty(msg)) {
      content = "<div class='msgs successMsg'><div class='msg-icon'></div><div class='msg-title'>"
          + "操作成功！"
          + "</div><div class='msg-txt'></div></div>";
    } else {
      content ="<div class='msgs successMsg'><div class='msg-icon'></div><div class='msg-title'>"
          + msg
          + "</div><div class='msg-txt'></div></div>"
    }
      top.layer.open({
      type: 1,
      title: false,
      closeBtn: 0,
      time:1000,
      shadeClose: true,
      skin: "msg",
      content: content
    });
  }
  function errorMsg(msg) {
    var content = "";
    if (isEmpty(msg)) {
      content = "<div class='msgs errorMsg'><div class='msg-icon'></div><div class='msg-title'>"
          + "操作失败！"
          + "</div><div class='msg-txt'></div></div>";
    } else {
      content ="<div class='msgs errorMsg'><div class='msg-icon'></div><div class='msg-title'>"
          + msg
          + "</div><div class='msg-txt'></div></div>"
    }
    top.layer.open({
      type: 1,
      title: false,
      closeBtn: 0,
      time:2000,
      shadeClose: true,
      skin: "msg",
      content: content
    });
  
  }
  function alertMsg(msg) {
    var content = "";
    if (isEmpty(msg)) {
      content = "<div class='msgs alertMsg'><div class='msg-icon'></div><div class='msg-title'>"
          + "操作有误！"
          + "</div><div class='msg-txt'></div></div>";
    } else {
      content ="<div class='msgs alertMsg'><div class='msg-icon'></div><div class='msg-title'>"
          + msg
          + "</div><div class='msg-txt'></div></div>"
    }
      top.layer.open({
      type: 1,
      title: false,
      closeBtn: 0,
      time:2000,
      shadeClose: true,
      skin: "msg",
      content: content
    });
  }
  function loadingMsg(msg) {
    var content = "";
    if (isEmpty(msg)) {
      content = "<div class='msg loadingMsg'><div class='msg-icon'></div><div class='msg-title'>"
          + "数据提交中，请稍候！"
          + "</div><div class='msg-txt'></div></div>";
    } else {
      content ="<div class='msg loadingMsg'><div class='msg-icon'></div><div class='msg-title'>"
          + msg
          + "</div><div class='msg-txt'></div></div>"
    }
    var indexLoading = layer.open({
      type: 1,
      title: false, //不显示标题
      closeBtn: 0,
      shadeClose: false,
      skin: "msg",
      content: content
    });
  
    return indexLoading;
  }
  
  function isEmpty(obj){
    if(typeof obj == "undefined" || obj == null || obj == "")	{
      return true;
    }else{
      return false;
    }
  }

function checkTime(i){
  if (i<10){
      i="0" + i
  }
  return i;
 }

function GMTToStr(time){
  let date = new Date(time)
  let Str=date.getFullYear() + '-' +
  (date.getMonth() + 1) + '-' +
  date.getDate() + ' ' +
  date.getHours() + ':' +
  date.getMinutes() + ':' +
  date.getSeconds()
  return Str
}

  //格式化时间(时间戳转换为 日期格式   年月日时分秒)
function formatDate(v) {
  if(/^(-)?\d{1,10}$/.test(v)) {
      v = v * 1000;
  } else if(/^(-)?\d{1,13}$/.test(v)) {
      v = v * 1;
  }
  var dateObj = new Date(v);
  var month = dateObj.getMonth() + 1;
  var day = dateObj.getDate();
  var hours = dateObj.getHours();
  var minutes = dateObj.getMinutes();
  var seconds = dateObj.getSeconds();
  if(month < 10) {
      month = "0" + month;
  }
  if(day < 10) {
      day = "0" + day;

  }
  if(hours < 10) {
      hours = "0" + hours;
  }
  if(minutes < 10) {
      minutes = "0" + minutes;
  }
  if(seconds < 10) {
      seconds = "0" + seconds;
  }
  var UnixTimeToDate = dateObj.getFullYear() + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds;
  return UnixTimeToDate;
}


function setForm(obj,jsonValue) {
  $.each(jsonValue, function (name, ival) {
      var $oinput = obj.find("[name=" + name + "]");
      if ($oinput.attr("type") == "radio" || $oinput.attr("type") == "checkbox") {
          $oinput.each(function() {
              if (Object.prototype.toString.apply(ival) == '[object Array]') { //是复选框，并且是数组
                  for (var i = 0; i < ival.length; i++) {
                      if ($(this).val() == ival[i]) //或者文本相等
                          $(this).prop("checked", true);
                  }
              } else {
                  if ($(this).val() == ival)
                      $(this).attr("selected",true);
              }
          });
      } else if ($oinput.attr("type") == "textarea") { //多行文本框
          obj.find("[name=" + name + "]").html(ival);
      } else if($oinput.attr("type") == "div") { //div
          $('#' + name).html(ival);
      } else {
          obj.find("[name=" + name + "]").val(ival);
      }
  });
}


function get_city_list(){
  city_list=[]
    $.ajax({
      type:"get",
      async:false,
      url:"/api/business/get_city_list/",
      success:function(result) {
          if (result.code = 200) { 
            city_list = result.data;
          } else {
              layer.msg(result.msg);
          }
      },
      error:function(result) {
          layer.msg("系统异常");
      }
  });
  return city_list
}

function get_city_select(){
  html = ''
  city_list = get_city_list()
  for(i=0;i<city_list.length;i++){
      text = '<option value='+city_list[i]+'>'+city_list[i]+'</option>'
      html = html+text
  }
  return html
}