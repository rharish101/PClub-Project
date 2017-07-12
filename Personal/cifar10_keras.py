import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from keras.layers.normalization import BatchNormalization
from keras.callbacks import TensorBoard
import pickle
import time

model = Sequential()

model.add(Conv2D(64, 2, 2, input_shape=(3, 32, 32), activation='relu',
	border_mode='same', dim_ordering='th'))
model.add(MaxPooling2D((2, 2), border_mode='same', dim_ordering='th'))
model.add(BatchNormalization(axis=1))

model.add(Conv2D(64, 3, 3, activation='relu', border_mode='same',
	dim_ordering='th'))
model.add(BatchNormalization(axis=1))
model.add(MaxPooling2D((2, 2), border_mode='same', dim_ordering='th'))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))

tb_callback = TensorBoard(log_dir='/home/rharish/Data/Tensorboard/' +\
	str(time.time()))

model.compile(loss='categorical_crossentropy', optimizer='adam',
	metrics=['accuracy'])

cifar10_train_images = []
cifar10_train_labels = []
for i in range(1, 6):
	train_file = open('cifar-10-batches-py/data_batch_' + str(i), 'r')
	train_dict = pickle.load(train_file)
	for image, label in zip(train_dict['data'], train_dict['labels']):
		image_red = np.reshape(image[:1024], (32, 32))
		image_green = np.reshape(image[1024:2048], (32, 32))
		image_blue = np.reshape(image[2048:3072], (32, 32))
		image = np.array([image_red, image_green, image_blue])
		cifar10_train_images.append(image)
		label = np.identity(10)[label]
		cifar10_train_labels.append(label)
	train_file.close()

cifar10_test_images = []
cifar10_test_labels = []
test_file = open('cifar-10-batches-py/test_batch', 'r')
test_dict = pickle.load(test_file)
for image, label in zip(test_dict['data'], test_dict['labels']):
	image_red = np.reshape(image[:1024], (32, 32))
	image_green = np.reshape(image[1024:2048], (32, 32))
	image_blue = np.reshape(image[2048:3072], (32, 32))
	image = np.array([image_red, image_green, image_blue])
	cifar10_test_images.append(image)
	label = np.identity(10)[label]
	cifar10_test_labels.append(label)
test_file.close()

model.fit(np.array(cifar10_train_images), np.array(cifar10_train_labels),
	nb_epoch=30, batch_size=64, callbacks=[tb_callback])

print(model.evaluate(np.array(cifar10_test_images),
	np.array(cifar10_test_labels), batch_size=256))
