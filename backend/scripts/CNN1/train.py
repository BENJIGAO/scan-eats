import os
from random import random
import numpy as np
from tensorflow import keras
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from cnn import CNN
from imutils import paths
import random
import cv2
from sklearn.preprocessing import LabelBinarizer
import pickle
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to input dataset (i.e., directory of images)")
ap.add_argument("-m", "--model", required=True,
	help="path to output model")
ap.add_argument("-l", "--labelbin", required=True,
	help="path to output label binarizer")
ap.add_argument("-p", "--plot", type=str, default="plot.png",
	help="path to output accuracy/loss plot")
args = vars(ap.parse_args())


# How many times network sees each training example and learns from it
EPOCHS = 100
# Default value for Adam optimizer used to train network
INIT_LR = 1e-3
# Will be passing batches of images into network for training
BATCH_SIZE = 32

data = []
labels = []

imagePaths = sorted(list(paths.list_images(args["dataset"])))
random.seed(42)
random.shuffle(imagePaths)


for imagePath in imagePaths:
    try:
        # load the image, pre-process it, and store it in the data list
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (150, 150))

        image = img_to_array(image)
        data.append(image)
        # extract the class label from the image path and update the
        # labels list
        label = imagePath.split(os.path.sep)[-2]
        labels.append(label)
    
    except:
        print('invalid')


# scale the raw pixel intensities to the range [0, 1]
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)
print("[INFO] data matrix: {:.2f}MB".format(
	data.nbytes / (1024 * 1000.0)))

# binarize the labels
lb = LabelBinarizer()
labels = lb.fit_transform(labels)
# partition the data into training and testing splits using 80% of
# the data for training and the remaining 20% for testing
(trainX, testX, trainY, testY) = train_test_split(data,
	labels, test_size=0.2, random_state=42)

# construct the image generator for data augmentation
# Gives model more images based on existing ones to train with.
aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1,
	height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	horizontal_flip=True, fill_mode="nearest")

# initialize the model
print("[INFO] compiling model...")
model = CNN.build()

model.compile(optimizer="adam", loss='binary_crossentropy', metrics=['accuracy'])

# train the network
print("[INFO] training network...")
model.fit(
	x=aug.flow(trainX, trainY, batch_size=BATCH_SIZE),
	validation_data=(testX, testY),
	steps_per_epoch=len(trainX) // BATCH_SIZE,
	epochs=EPOCHS, verbose=1)

# save the model to disk
print("[INFO] serializing network...")
model.save("orange.model", save_format="h5")
# save the label binarizer to disk
print("[INFO] serializing label binarizer...")
f = open("orange.pickle", "wb")
f.write(pickle.dumps(lb))
f.close()




# train = ImageDataGenerator(rescale=1/255)
# test = ImageDataGenerator(rescale=1/255)

# train_dataset = train.flow_from_directory("C:/Users/Admin/Desktop/code/scan-eats/data/foods/bananas",
#                                           target_size=(150,150),
#                                           batch_size = 32,
#                                           class_mode = 'binary')
                                         
# test_dataset = test.flow_from_directory("C:/Users/Admin/Desktop/code/scan-eats/data/foods/bananas",
#                                           target_size=(150,150),
#                                           batch_size =32,
#                                           class_mode = 'binary')

# model = CNN.buid()
# model.compile(optimizer='adam',loss='binary_crossentropy', metrics=['accuracy'])

# #steps_per_epoch = train_imagesize/batch_size
# model.fit_generator(train_dataset,
#          steps_per_epoch = 250,
#          epochs = 10,
#          validation_data = test_dataset
# )