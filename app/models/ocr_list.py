import pytesseract
from PIL import Image
import requests
from io import BytesIO
from cnocr import CnOcr

def pytesseract_ocr(url, lang='chi_sim'):
    # 导入OCR安装路径，如果设置了系统环境，就可以不用设置了
    pytesseract.pytesseract.tesseract_cmd = r"D:\App\Tesseract-OCR\tesseract.exe"
    # 打开要识别的图片
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    # 使用pytesseract调用image_to_string方法进行识别，传入要识别的图片，lang='chi_sim'是设置为中文识别，
    text = pytesseract.image_to_string(image, lang= lang)
    return text

def cnocr_ocr(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    ocr = CnOcr(rec_model_name='ch_PP-OCRv3')
    out = ocr.ocr(image)
    result = ''
    for x in out:
        result += x["text"]
        result += "\n"
    return result