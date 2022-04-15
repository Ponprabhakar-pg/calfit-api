from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from random import randint

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_IMAGES'] = os.getcwd() + '\\upload_images'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'jfif']

DUMMY_FOODS = ['sambar', 'idly', 'dosa', 'vada', 'chuttney', 'poori', 'chapathi', 'pongal']
DUMMY_CALORIES = [41.2, 52.1, 50.1, 68.0, 21.3, 78.4, 31.5, 10.4]


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def default():
    return 'Welcome to Calfit!'


@app.route('/file-upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if os.path.exists(app.config['UPLOAD_IMAGES']):
            file.save(os.path.join(app.config['UPLOAD_IMAGES'], filename))
        else:
            os.mkdir(app.config['UPLOAD_IMAGES'])
            file.save(os.path.join(app.config['UPLOAD_IMAGES'], filename))
        resp = jsonify(
            {
                'food_name': DUMMY_FOODS[randint(0, len(DUMMY_FOODS))],
                'calorie_detected': DUMMY_CALORIES[randint(0, len(DUMMY_CALORIES))]
            }
        )
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are png, jpg, jpeg, gif, jfif'})
        resp.status_code = 400
        return resp


if __name__ == '__main__':
    app.run()
