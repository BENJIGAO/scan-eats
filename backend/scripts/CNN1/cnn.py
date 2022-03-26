from tensorflow import keras

class CNN:
    @staticmethod
    def build():
        model = keras.Sequential()

        # Convolutional layer and maxpool layer 1
        model.add(keras.layers.Conv2D(32,(3,3),activation='relu',input_shape=(150,150,3)))
        model.add(keras.layers.MaxPool2D(2,2))

        # Convolutional layer and maxpool layer 2
        model.add(keras.layers.Conv2D(64,(3,3),activation='relu'))
        model.add(keras.layers.MaxPool2D(2,2))

        # Convolutional layer and maxpool layer 3
        model.add(keras.layers.Conv2D(128,(3,3),activation='relu'))
        model.add(keras.layers.MaxPool2D(2,2))

        # Convolutional layer and maxpool layer 4
        model.add(keras.layers.Conv2D(128,(3,3),activation='relu'))
        model.add(keras.layers.MaxPool2D(2,2))

        # This layer flattens the resulting image array to 1D array
        model.add(keras.layers.Flatten())

        # Hidden layer with 512 neurons and Rectified Linear Unit activation function 
        model.add(keras.layers.Dense(512,activation='relu'))

        # Output layer with single neuron which gives 0 for Cat or 1 for Dog 
        #Here we use sigmoid activation function which makes our model output to lie between 0 and 1
        model.add(keras.layers.Dense(1,activation='sigmoid'))

        return model