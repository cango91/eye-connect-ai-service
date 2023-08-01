import os
import dotenv
import cv2
import io
from keras.models import load_model
from keras.utils import img_to_array, load_img
from flask import Flask, request, abort, jsonify

dotenv.load_dotenv()

API_KEY = os.environ.get('API_KEY')

app = Flask(__name__)
model = load_model('model.h5')

ALPHA = 4
BETA = -4
GAMMA = 128
BLR_SIZE = (0, 0)
BLR_DEV = 10

# preprocess the image 
def pp(img):
    return cv2.addWeighted(img,
                           ALPHA,
                           cv2.GaussianBlur(img, BLR_SIZE, BLR_DEV),
                           BETA,
                           GAMMA)

# run the model, return the prediction
def run_model(model, img):
    img = img.reshape(1, 512, 512, 3)
    prediction = model.predict(img)
    return prediction


@app.before_request
def before_request():
    if request.headers.get('X-Api-Key') != os.environ.get('API_KEY'):
        abort(401)  # Unauthorized

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify(error='No image file'), 400
    file = request.files['image']
    img = load_img(io.BytesIO(file.read()),target_size=(512,512))
    img = img_to_array(img)
    img = pp(img)
    prediction = run_model(model, img)
    return {'prediction': prediction.tolist()}

if __name__ == '__main__':
    app.run(host='localhost', port=5001)
