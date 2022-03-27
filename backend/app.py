import os
from flask import Flask, render_template, request
from scripts.CNN1.classify import predict_image
from reverse_proxy import proxy_request

MODE = os.getenv('FLASK_ENV')
DEV_SERVER_URL = "http://localhost:3000/"

app = Flask(__name__)

# Two modes: Development and Production mode
# Ignore static folder in development mode
if MODE == "development":
    app = Flask(__name__, static_folder=None)

@app.route('/')
@app.route('/<path:path>')
def index(path=''):
    if MODE == 'development':
        return proxy_request(DEV_SERVER_URL, path)
    
    else:
        return render_template("index.html")

@app.route('/classify/banana', methods=['POST'])
def banana_classify():
    if (request.files['image']):
        image = request.files['image']

        result = predict_image(image, os.path.abspath(r"..\backend\scripts\CNN1\banana.model"), "banana")
        print('Model classification: ' + result)
        return result

@app.route('/classify/apple', methods=['POST'])
def apple_classify():
    if (request.files['image']):
        image = request.files['image']
        print(os.path.abspath("scripts\CNN1\apple.model"))

        result = predict_image(image, os.path.abspath(r"..\backend\scripts\CNN1\apple.model"), "apple")
        print('Model classification: ' + result)
        return result