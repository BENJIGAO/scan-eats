""" lenet_dataset
Handles:
1. Loading the dataset
2. Partitioning dataset into training and testing splits
3. Loading and compiling the LeNet architecture.
4. Training the network.
5. Optionally saving the serialized network weights
to disk so that it can be resused. (Don't have to re-train the network)
6. Displaying visual examples of the network output to demonstrate
that the implementation is working.
"""
from pyimagesearch.cnn.networks.lenet import LeNet
from sklearn.model_selection import train_test_split
from keras.datasets import mnist
from keras.optimizers import SGD
from keras.utils import np_utils
from keras import backend as K
import numpy as np
import argparse
import cv2

# construct the argument parser and parse the arguments
# --save-model: Specify whether to save model to disk after training
# --load-model: Spcify whether to load model from pre-trained one from disk
# --weights: If --save-model is True, this points to where to save model
# If --load-model is True, this points to where pre-trained model is on disk.
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--save-model", type=int, default=-1,
	help="(optional) whether or not model should be saved to disk")
ap.add_argument("-l", "--load-model", type=int, default=-1,
	help="(optional) whether or not pre-trained model should be loaded")
ap.add_argument("-w", "--weights", type=str,
	help="(optional) path to weights file")
args = vars(ap.parse_args())


# if we are using "channels first" ordering, then reshape the
# design matrix such that the matrix is:
# num_samples x depth x rows x columns
if K.image_data_format() == "channels_first":
	trainData = trainData.reshape((trainData.shape[0], 1, 28, 28))
	testData = testData.reshape((testData.shape[0], 1, 28, 28))
# otherwise, we are using "channels last" ordering, so the design
# matrix shape should be: num_samples x rows x columns x depth
else:
	trainData = trainData.reshape((trainData.shape[0], 28, 28, 1))
	testData = testData.reshape((testData.shape[0], 28, 28, 1))
# scale data to the range of [0, 1]
trainData = trainData.astype("float32") / 255.0
testData = testData.astype("float32") / 255.0