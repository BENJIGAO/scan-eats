from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras import backend as K

class LeNet:
    @staticmethod
    def build(numChannels, imgRows, imgCols, numClasse,
        activation="relu", weightsPath=None):
        # initialize the model
        model = Sequential()
        inputShape = (imgRows, imgCols, numChannels)
        