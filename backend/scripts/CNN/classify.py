from cProfile import label
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os


def get_prediction(image_path, model_path="train.model", label_path="lb.pickle"):
    # Load the image
    image = cv2.imread(image_path)
    output = image.copy()

    # Pre-process the image for classification
    image = cv2.resize(image, (96, 96))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    # Load the trained CNN and label binarizer
    model = load_model(model_path)

    proba = model.predict(image)[0]

    # Mark prediction as "correct" if the input image filename
    # contains the predicted label text
    return proba

def classify_image(image_path, model_path="train.model", label_path="lb.pickle"):
    proba = get_prediction(image_path, model_path, label_path)
    lb = pickle.loads(open(label_path, "rb").read())
    idx = np.argmax(proba)
    label = lb.classes_[idx]

    result = "{}: {:.2f}%".format(label, proba[idx] * 100)

    return result

    

# # we'll mark our prediction as "correct" of the input image filename
# # contains the predicted label text (obviously this makes the
# # assumption that you have named your testing image files this way)
# filename = args["image"][args["image"].rfind(os.path.sep) + 1:]
# correct = "incorrect" if filename.rfind(label) != -1 else "correct"
# # build the label and draw the label on the image
# # if proba[idx] * 100 > 50:
# #     correct = "correct"

# # else:
# #     correct = "incorrect"

# label = "{}: {:.2f}% ({})".format(label, proba[idx] * 100, correct)
# output = imutils.resize(output, width=400)
# cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
# 	0.7, (0, 255, 0), 2)
# # show the output image
# print("[INFO] {}".format(label))
# cv2.imshow("Output", output)
# cv2.waitKey(0)





# construct the argument parser and parse the arguments
# --model: Path to the model we trained
# --labelbin: Path to the label binarizer file.
# --image: Path to input image file.

# ap = argparse.ArgumentParser()
# ap.add_argument("-m", "--model", required=True,
# 	help="path to trained model model")
# ap.add_argument("-l", "--labelbin", required=True,
# 	help="path to label binarizer")
# ap.add_argument("-i", "--image", required=True,
# 	help="path to input image")
# args = vars(ap.parse_args())

# # load the image
# image = cv2.imread(args["image"])
# output = image.copy()
 
# # pre-process the image for classification
# image = cv2.resize(image, (96, 96))
# image = image.astype("float") / 255.0
# image = img_to_array(image)
# image = np.expand_dims(image, axis=0)

# # load the trained convolutional neural network and the label
# # binarizer
# print("[INFO] loading network...")
# model = load_model(args["model"])
# lb = pickle.loads(open(args["labelbin"], "rb").read())
# # classify the input image
# print("[INFO] classifying image...")
# proba = model.predict(image)[0]
# idx = np.argmax(proba)
# label = lb.classes_[idx]

# # we'll mark our prediction as "correct" of the input image filename
# # contains the predicted label text (obviously this makes the
# # assumption that you have named your testing image files this way)
# filename = args["image"][args["image"].rfind(os.path.sep) + 1:]
# correct = "incorrect" if filename.rfind(label) != -1 else "correct"
# # build the label and draw the label on the image
# # if proba[idx] * 100 > 50:
# #     correct = "correct"

# # else:
# #     correct = "incorrect"

# label = "{}: {:.2f}% ({})".format(label, proba[idx] * 100, correct)
# output = imutils.resize(output, width=400)
# cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
# 	0.7, (0, 255, 0), 2)
# # show the output image
# print("[INFO] {}".format(label))
# cv2.imshow("Output", output)
# cv2.waitKey(0)