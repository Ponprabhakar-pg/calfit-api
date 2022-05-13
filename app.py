from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import pymongo

app = Flask(__name__)
CORS(app)

myclient = pymongo.MongoClient("mongodb+srv://pg:prabha%40atlas@cluster0.uvmcv.mongodb.net/")
mydb = myclient["CalFit"]
mycol = mydb['FoodCalorieData']

app.config['UPLOAD_IMAGES'] = os.getcwd() + '\\upload_images'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'jfif']

# DUMMY_FOODS = ['sambar', 'idly', 'dosa', 'vada', 'chuttney', 'poori', 'chapathi', 'pongal']
# DUMMY_CALORIES = [41.2, 52.1, 50.1, 68.0, 21.3, 78.4, 31.5, 10.4]


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def train_image(image):
    print(image)
    return 'adai'

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
        foodName = train_image(app.config['UPLOAD_IMAGES'])
        data = []
        try:
            for x in mycol.find({"FoodName": foodName}):
                x["_id"] = str(x["_id"])
                data.append(x)
        except:
            resp = jsonify({'message': 'Something went wrong.'})
            return resp
        resp = []
        for datum in data:
            temp = {
                'food_name': datum['FoodName'],
                'calorie_detected': datum['Calories']
            }
            resp.append(temp)
        return jsonify(resp)
    else:
        resp = jsonify({'message': 'Allowed file types are png, jpg, jpeg, gif, jfif'})
        return resp


if __name__ == '__main__':
    app.run('0.0.0.0')
