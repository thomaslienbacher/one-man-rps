import os
from tensorflow import keras

IMG_NET_SIZE = (96, 96)


def save_model(directory, model):
    path = os.path.join(directory, "model_weights.h5")
    model.save_weights(path)

    path = os.path.join(directory, "model_architecture.json")
    with open(path, "w") as f:
        f.write(model.to_json())
    print("Saved model!")


def create_model():
    model = keras.Sequential([
        keras.layers.Conv2D(32, (5, 5), activation='relu', input_shape=(IMG_NET_SIZE[0], IMG_NET_SIZE[1], 1)),
        keras.layers.MaxPooling2D((3, 3)),
        keras.layers.Conv2D(64, (5, 5), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        # keras.layers.Conv2D(64, (5, 5), activation='relu'),
        # keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dropout(0.4),
        keras.layers.Dense(72, activation='relu'),
        keras.layers.Dropout(0.1),
        keras.layers.Dense(4, activation='softmax')
    ])

    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model
