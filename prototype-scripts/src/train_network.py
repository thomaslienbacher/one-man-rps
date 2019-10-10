"""
Dieses Script nimmt trainiert ein Neural Netzwerk, mit den Daten die vorher
aufbereitet wurden.
"""

import tensorflow as tf
from tensorflow import keras
import pickle
import os

DATADIR = "E:/Thomas/one-man-rps/data"
SIZE = (64, 64)

path = os.path.join(DATADIR, "X.pickle")
pickle_in = open(path, "rb")
X = pickle.load(pickle_in)

path = os.path.join(DATADIR, "y.pickle")
pickle_in = open(path, "rb")
y = pickle.load(pickle_in)

X = X / 255.0

model = keras.Sequential([
    keras.layers.Flatten(input_shape=SIZE),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(24, activation=tf.nn.relu),
    keras.layers.Dense(3, activation=tf.nn.softmax)
])

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

path = os.path.join(DATADIR, "logs")
tensorboard = keras.callbacks.TensorBoard(log_dir=path)
model.fit(X, y, batch_size=32, epochs=12, validation_split=0.2, callbacks=[tensorboard])
model.summary()
print("Trained model!")

path = os.path.join(DATADIR, "model_64x64.h5")
model.save(path)
print("Saved model!")
