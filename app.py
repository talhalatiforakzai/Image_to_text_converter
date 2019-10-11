import io
import os

import pytesseract
import requests
from PIL import Image
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/image_to_text', methods=['POST'])
def image_to_text():
    try:
        img = Image.open(request.files['file'].stream)
        return converter(img)
    except:
        return jsonify(
            {"error": "Did you mean to send: {'file': 'some_image'}"}
        )


@app.route('/url_to_text', methods=['POST'])
def url_to_text():
    try:
        url = request.get_json('image_url')
        url = url['image_url']
        if os.path.isfile(url):
            return converter(url)
        else:
            response = requests.get(url)
            img = Image.open(io.BytesIO(response.content))
            return converter(img)
    except:
        return jsonify(
            {"error": "Did you mean to send: {'image_url': 'some_image_url_path'}"}
        )


def converter(img):
    txt = pytesseract.image_to_string(img, config="--psm 6")
    return jsonify({"Text": repr(txt)})


if __name__ == '__main__':
    app.run
