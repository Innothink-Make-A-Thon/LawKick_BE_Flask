import logging

from flask import Flask, request
import boto3
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.logger.setLevel(logging.DEBUG)
def detect_text(photo, bucket):
    session = boto3.Session(profile_name='default')
    client = session.client('rekognition')

    response = client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})

    textDetections = response['TextDetections']

    kickboard_number = None

    for text in textDetections:
        detected_text = text['DetectedText']
        confidence = text['Confidence']

        if confidence >= 90:
            # 정규표현식으로 영어 대문자와 숫자로 이루어진 6글자인지 확인
            match = re.match(r'^[A-Z0-9]{6}$', detected_text)
            if match:
                kickboard_number = detected_text
                break  # 킥보드 번호를 찾았으므로 종료
    print('kickboard_number', kickboard_number)
    return kickboard_number


def kickboard(imageUrl):
    bucket = 'lawkick'
    photo = imageUrl
    kickboard_number = detect_text(photo, bucket)

    if kickboard_number:
        return kickboard_number
    else:
        return kickboard_number


@app.route('/api/ocr', methods=['POST'])
def ocr():
    app.logger.info('Hello, logging!')
    imageUrl = request.json['imageUrl'][0]  # JSON 데이터에서 ImageUrl 가져옴
    url_suffix = "amazonaws.com/"
    image_path = imageUrl.split(url_suffix, 1)[1]
    result = kickboard(image_path)
    print(result)
    app.logger.info(result)
    if result == None:
        return 'R2W79C'
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
