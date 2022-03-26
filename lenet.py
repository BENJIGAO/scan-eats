from multiprocessing import pool
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras import backend as K

# numChannels = depth of our input images
# imgCols = width of input image
# imgRows = height of input images
class LeNet:
    @staticmethod
    def build(numChannels, imgRows, imgCols, numClasses,
        activation="relu", weightsPath=None):
        # initialize the model
        model = Sequential()
        inputShape = (imgRows, imgCols, numChannels)
        
        # Channels First = [channels][rows][cols]
        # Channels Last = [rows][cols][channels]
        # if we are using "channels first", update the input shape
        if K.image_data_format() == "channels_first":
            inputShape = (numChannels, imgRows, imgCols)
        
        # First sert of Conv => ACTIVATION => POOL Layers
        # Conv2D(filters, kernels, padding, input_shape)
        model.add(Conv2D(20, 5, padding="same",
              input_shape = inputShape))
        model.add(Activation(activation))

        # 2x2 convolution matrix that takes a step of 2 pixels 
        # horizontally and vertically.
        model.add(MaxPooling2D(pool_size=(2, 2), striders = (2, 2)))
    
        # Second set of CONV => ACTIVATION => POOL Layers
        # Num of convolutional filters increase as layers deepen in
        # network
        model.add(Conv2D(50, 5, padding="same"))
        model.add(Activation(activation))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        # Fully connected layers (Dense layers)
        # Define the first FC => ACTIVATION layers

        model.add(Flatten()) # Flatten last output of MaxPooling2D layer
        # Represents 500 units in Dense layer
        model.add(Dense(500))
        model.add(Activation(activation))

        # define the second FC layer
        # numClasses = number of images model will learn
        # Ex: Banana dataset has 3 categories to learn
        model.add(Dense(numClasses)) 
        
        # lastly, define the soft-max classifier\
        # Returns a list of probabilities for each of the
        # numClasses labels
        # Class label with the largest probability will be chosen 
        # as final classification from network
        model.add(Activation("softmax"))

        # if a weights path is supplied (inicating that the model was
        # pre-trained), then load the weights
        if weightsPath is not None:
            model.load_weights(weightsPath)
            
        # return the constructed network architecture
        return model