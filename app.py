from flask import Flask, request, jsonify
import os
from PIL import Image
from pytesseract import *


app = Flask(__name__)


@app.route('/api/ocr', methods=['POST'])
def ocr():
    file = request.files['file']  # 요청에서 파일을 가져옴

    # 임시 파일을 생성하고 저장
    temp_path = "temp_file.jpg"
    file.save(temp_path)

    image = Image.open(temp_path)
    print(image)
    result = image_to_string(image, lang='eng', config='--psm 1 -c preserve_interword_spaces=1' )
    print(result, '===============', type(result))
    # 임시 파일 삭제
    os.remove(temp_path)
    # 결과를 JSON 형태로 반환
    return jsonify({'output_data': result})


if __name__ == '__main__':
    app.run(debug=True)