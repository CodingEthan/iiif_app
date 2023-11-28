let fileInput = document.getElementById('file');
let info = document.getElementById('info');
let preview = document.getElementById('image-preview');
// 监听change事件:
fileInput.addEventListener('change', function () {
  // 清除背景图片:
  preview.style.backgroundImage = '';
  if (!fileInput.value) {
    info.innerHTML = '未选择文件';
    return;
  }
  let file = fileInput.files[0];
  let size = file.size;
  if (size >= 1 * 1024 * 1024) {
    alert('文件大小超出限制');
    info.innerHTML = '文件大小超出限制';
    return false;
  }
  // 获取File信息:
  info.innerHTML = `文件名称:  + ${file.name}<br>文件大小: ${file.size} <br>上传时间: ${file.lastModifiedDate}`;
  if (!['image/jpeg', 'image/png', 'image/gif'].includes(file.type)) {
    alert('不是有效的图片文件!');
    return;
  }
  // 读取文件:
  let reader = new FileReader();
  reader.onload = function (e) {
    let data = e.target.result;
    console.log(preview, 'a标签')
    preview.src = data
  };
  // 以DataURL的形式读取文件:
  reader.readAsDataURL(file);

});

function save() {

  var url = preview.src; // 获取图片地址
  var a = document.createElement('a'); // 创建一个a节点插入的document
  var event = new MouseEvent('click') // 模拟鼠标click点击事件
  a.download = 'beautifulGirl' // 设置a节点的download属性值
  a.href = url; // 将图片的src赋值给a节点的href
  a.dispatchEvent(event)
};

$("#photo_submit").click(function () {
  let formData = new FormData();
  let fileObj = document.getElementById('file').files[0];
  if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
    alert("请选择图片");
    return;
  }
  // @Param: myFile.file[0]为第一个文件（单选）,多个文件（多选）则要循环添加
  formData.append('file', fileObj);
  $.ajax({
    url: "/uplord",
    data: formData,
    type: "post",
    dataType: "json",
    cache: false,//上传文件无需缓存
    processData: false,//用于对data参数进行序列化处理 这里必须false
    contentType: false, //必须
    success: function (data) {
      alert(data.result);
    },
    error: function (jqXHR) {
      // 这里是访问失败时被自动调用的代码
      alert(jqXHR);
    }
  })
});