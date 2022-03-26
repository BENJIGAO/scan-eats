import os
from flask import Flask, render_template, request
from backend.scripts.CNN.classify import classify_image
from backend.reverse_proxy import proxy_request

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

@app.route('/classify', methods=['POST'])
def classify():
    if (request.files['image']):
        image_path = request.files(['image'])

        result = classify_image(image_path)
        print('Model classification: ' + result)
        return result