"""
Dieses Script nimmt trainiert ein Neural Netzwerk, mit den Daten die vorher
aufbereitet wurden.
"""


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

model = keras.Sequential([
    keras.layers.Conv2D(32, (5, 5), activation='relu', input_shape=(SIZE[0], SIZE[1], 1)),
    keras.layers.MaxPooling2D((3, 3)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(3, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

path = os.path.join(DATADIR, "logs")
tensorboard = keras.callbacks.TensorBoard(log_dir=path)
model.fit(X, y, batch_size=200, epochs=6, validation_split=0.05, callbacks=[tensorboard])
model.summary()
print("Trained model!")

path = os.path.join(DATADIR, "model_weights.h5")
model.save_weights(path)

path = os.path.join(DATADIR, "model_architecture.json")
with open(path, "w") as f:
    f.write(model.to_json())
print("Saved model!")
