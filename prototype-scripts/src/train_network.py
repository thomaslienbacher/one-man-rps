"""
Dieses Script nimmt trainiert ein Neural Netzwerk, mit den Daten die vorher
aufbereitet wurden.
"""


from tensorflow import keras
import pickle
import os
from utils import *

DATADIR = "E:/Thomas/one-man-rps/data"

path = os.path.join(DATADIR, "X.pickle")
pickle_in = open(path, "rb")
X = pickle.load(pickle_in)

path = os.path.join(DATADIR, "y.pickle")
pickle_in = open(path, "rb")
y = pickle.load(pickle_in)

model = create_model()

path = os.path.join(DATADIR, "logs")
tensorboard = keras.callbacks.TensorBoard(log_dir=path, histogram_freq=0)
model.fit(X, y, batch_size=200, epochs=4, validation_split=0.5, callbacks=[tensorboard])
model.summary()
print("Trained model!")

save_model(DATADIR, model)
