from typing import io

from flask import Flask, request
import io
from PIL import Image
from pytesseract import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/ocr', methods=['POST'])
def ocr():
    file = request.files['file']  # 요청에서 파일을 가져옴

    image_bytes = io.BytesIO(file.read())

    # BytesIO로 읽어온 이미지를 Image로 변환
    image = Image.open(image_bytes)

    # 이미지 처리
    result = image_to_string(image, lang='eng', config='--psm 1 -c preserve_interword_spaces=1')

    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)