from app.router import app
from PIL import Image
from flask import Response
from PIL import Image
import io


@app.route('/<identifier>/<region>/<size>/<rotation>/<quality>.<format>')
def iiif(identifier, region, size, rotation, quality, format):
    image_path = "app/static/img/%s" % identifier + ".%s" % format
    # 打开图像
    with Image.open(image_path) as img:
        # 确定图像区域
        if region == 'full':
            img_region = img
        else:
            region_params = region.split(',')
            x, y, w, h = map(int, region_params)
            img_region = img.crop((x, y, x + w, y + h))

        # 确定图像大小
        if size == 'full':
            img_size = img_region
        else:
            size_params = size.split(',')
            w, h = map(int, size_params)
            img_size = img_region.resize((w, h))

        # 旋转图像
        if rotation != '0':
            angle = float(rotation)
            img_size = img_size.rotate(angle, expand=True)

        # 确定图像质量
        if quality != 'default':
            img_quality = img_size.convert('RGB').save(None, quality=quality)
        else:
            img_quality = img_size

        # 创建响应对象
        response = Response()
        response.status_code = 200
        response.headers['Content-Type'] = 'image/jpeg'

        # 将图像写入响应对象
        img_io = io.BytesIO()
        img_quality.save(img_io, format='JPEG')
        response.data = img_io.getvalue()

        return response
