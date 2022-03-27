from cProfile import label
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from numpy import expand_dims
from PIL import ImageFile, Image
import argparse
import imutils
import pickle
import cv2
import os


def predict_image(file_path, model_path):

    # img1 = image.load_img(file_path, target_size=(150, 150))
    # Y = image.img_to_array(file_path)
    # X = np.expand_dims(Y, axis=0)
    # model = load_model(model_path)
    # val = model.predict(X)
    # print(val)
    model = load_model(model_path)

    original_image = Image.open(file_path)
    original_image = original_image.convert('RGB')
    original_image = original_image.resize((150, 150), Image.NEAREST)
    numpy_image = image.img_to_array(original_image)
    image_batch = expand_dims(numpy_image, axis=0)

    processed_image = preprocess_input(image_batch, mode='caffe')
    preds = model.predict(processed_image)

    if model_path == "orange.model":
        if preds == 1:
            return "fresh"
        else: 
            return "stale"
    else:
        if preds == 1:
            return "stale"

        else:
            return "fresh"

"""
def get_prediction(image_path, model_path, label_path):
    # Load the image
    image = cv2.imread(image_path)
    output = image.copy()

    # Pre-process the image for classification
    image = cv2.resize(image, (150, 150))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    # Load the trained CNN and label binarizer
    model = load_model(model_path)

    proba = model.predict(image)[0]

    # Mark prediction as "correct" if the input image filename
    # contains the predicted label text
    return proba

def classify_image(image_path, model_path, label_path):
    proba = get_prediction(image_path, model_path, label_path)
    lb = pickle.loads(open(label_path, "rb").read())
    idx = np.argmax(proba)
    label = lb.classes_[idx]

    result = "{}: {:.2f}%".format(label, proba[idx] * 100)

    return result
"""