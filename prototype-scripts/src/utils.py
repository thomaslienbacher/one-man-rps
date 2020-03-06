"""
In diesem Script werden Funktionen und Konstanten definiert die in mehreren anderen Scripts benutzt werden.
"""

import os
from datetime import datetime

from tensorflow import keras

IMG_NET_SIZE = (128, 128)


def time_escaped():
    now_escaped = str(datetime.now()).replace(":", "_").replace(".", "_").replace(" ", "T")
    return now_escaped


def save_model(directory, model):
    path = os.path.join(directory, "model_weights_" + time_escaped() + ".h5")
    model.save_weights(path)

    path = os.path.join(directory, "model_architecture_" + time_escaped() + ".json")
    with open(path, "w") as f:
        f.write(model.to_json())
    print("Saved model!")


def create_model():
    model = keras.Sequential([
        keras.layers.Conv2D(32, (5, 5), activation='relu', input_shape=(IMG_NET_SIZE[0], IMG_NET_SIZE[1], 1)),
        keras.layers.MaxPooling2D((3, 3)),
        keras.layers.Conv2D(64, (5, 5), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(56, (5, 5), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dropout(0.30),
        keras.layers.Dense(70, activation='relu'),
        keras.layers.Dropout(0.09),
        keras.layers.Dense(4, activation='softmax')
    ])

    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model
