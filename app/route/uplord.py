import uuid
from flask import request, render_template, jsonify, render_template, redirect, send_file
from app.router import app
from flask import Flask, jsonify, request, render_template
from PIL import Image
import json as js
from app.models.ocr_list import cnocr_ocr, pytesseract_ocr
from app.models.chatgpt_api import completion


@app.route('/iiif/make_manifest', methods=['GET', 'POST'])
def make_manifest():
    if request.method == "GET":
        return render_template('make_manifest.html')
    else:
        identifier = request.form['identifier']
        iiif_url = request.form['iiif_url']
        typeface = request.form['typeface']
        with open('app\static\manifest\manifest_template.json', 'r', encoding='utf-8') as f:
            manifest_dict = js.load(f)
        text = pytesseract_ocr(iiif_url,lang=typeface)
        # if typeface == "chi_sim":
        #     text = cnocr_ocr(iiif_url)
        # else:
        #     text = pytesseract_ocr(iiif_url)
        try:
            request.form['ChatGPT']
            prompt = "详细解释：" + text
            reponse = completion(prompt)
            manifest_dict["metadata"][0]["label"] = "chatgpt分析结果"
            manifest_dict["metadata"][0]["value"] = reponse
        finally:
            manifest_dict["@id"] = "http://localhost:8000/iiif/%s/manifest.json" % identifier
            manifest_dict["description"] = text
            manifest_dict["sequences"][0]["canvases"][0]["images"][0]["@id"] = iiif_url
            manifest_dict["sequences"][0]["canvases"][0]["images"][0]["resource"]["@id"] = iiif_url
            json = js.dumps(manifest_dict)
            json_path = 'app\static\manifest\%s.json' % identifier
            with open(json_path, 'w', encoding='utf-8') as file:
                file.write(json)
            return render_template('viewer.html')


@app.route('/iiif/<identifier>/manifest.json')
def manifest(identifier):
    with open('app\static\manifest\%s.json' % identifier, 'r', encoding='utf-8') as file:
        manifest = file.read()
    return jsonify(manifest)


@app.route('/')
def home_page():
    return render_template('home_page.html')


@app.route('/uplord', methods=['GET', 'POST'])
def uplord():
    if request.method == "GET":
        return render_template('home_page.html')
    else:
        if 'file' in request.files:
            file = request.files['file']
            filename = str(uuid.uuid4())
            filepath = "app/static/img/%s.jpg" % filename
            file.save(filepath)
            return jsonify({"result": "上传成功,IIIF_URL: http://localhost:8000/%s/full/full/0/default.jpg" % filename})
        else:
            return jsonify({"result": "上传错误，请重试"})


# # 创建清单对象
# manifest = IIIFManifest()

# # 添加元数据信息
# iiif_prezi3.MakeManifest
# manifest.set_name("Example Manifest")
# manifest.set_description("This is an example manifest")

# # 创建画布对象
# canvas = IIIFCanvas()

# # 添加图像信息
# image = IIIFImage("http://example.com/image.jpg")
# image.set_size(width=800, height=600)
# image.set_format("jpg")

# # 添加图像到画布中
# canvas.add_image(image)

# # 添加画布到清单中
# manifest.add_canvas(canvas)

# # 生成清单JSON字符串
# manifest_json = manifest.to_json()

# # 输出清单JSON字符串
# print(manifest_json)
