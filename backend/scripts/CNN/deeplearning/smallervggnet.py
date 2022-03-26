from multiprocessing import pool
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense
from tensorflow.keras import backend as K

class SmallerVGGNet:
    @staticmethod
    def build(width, height, depth, classes):
        # initialize model along with input shape to be
        # channels last and the channel dimensions itself
        # Channels First = [channels][rows][cols]
        # Channels Last = [rows][cols][channels]
        model = Sequential()
        inputShape = (height, width, depth)
        chanDim = -1

        # if using channel first, update input shape and channel dim
        if K.image_data_format() == "channels_first":
            inputShape = (depth, height, width)
            chanDim = 1
        
        # First Layer of
        # CONV => RELU => POOL
        # Convolution Layer: 32 filters, 3 x 3 kernel
        model.add(Conv2D(32, (3, 3), padding="same",
              input_shape=inputShape))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        
        # 3 x 3 POOl size
        # 3 x 3 convolution matrix moving at 1 x 1 pixels across image
        model.add(MaxPooling2D(pool_size=(3, 3)))

        # 25% of nodes are disconnected from this layer to the next
        model.add(Dropout(0.25))

        # Second layer of (CONV => RELU) * 2 => POOL
        # filter size increases as layers increase
        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))

        # Pool size decreased from 3x3 to 2x2 to ensure 
        # spatial dimensions aren't reduced too quickly.
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        # Third set of: (CONV => RELU) * 2 => POOL:
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        # Final set of FC => RELU Layers
        # Flatten last output from MaxPooling2D layer
        model.add(Flatten())
        model.add(Dense(1024)) # 1024 units in the Dense layer
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        # softmax classifier
        model.add(Dense(classes))

        # Returns the predicted probabilities for each class label
        model.add(Activation("softmax"))

        # return the constructed network architecture
        return model