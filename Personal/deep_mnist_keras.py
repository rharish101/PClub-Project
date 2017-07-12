import numpy as np
from keras.models import Sequential
model = Sequential()

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/")

from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout

model.add(Conv2D(32, 5, 5, input_shape=(28, 28, 1),
	activation='relu', border_mode='same'))
model.add(MaxPooling2D((2, 2), border_mode='same'))
model.add(Dropout(0.25))

model.add(Conv2D(64, 3, 3, activation='relu', border_mode='same'))
model.add(MaxPooling2D((2, 2), border_mode='same'))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy',
				optimizer='adam',
				metrics=['accuracy'])

x_train = np.resize(mnist.train.images, (
	mnist.train.images.shape[0], 28, 28, 1))
y_train = np.array([np.identity(10)[y] for y in mnist.train.labels])

model.fit(x_train, y_train, nb_epoch=25, batch_size=100)

x_test = np.resize(mnist.test.images, (
	mnist.test.images.shape[0], 28, 28, 1))
y_test = np.array([np.identity(10)[y] for y in mnist.test.labels])

print(model.evaluate(x_test, y_test, batch_size=200))
