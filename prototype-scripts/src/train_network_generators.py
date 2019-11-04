"""
Dieses Script trainiert ein Neural Netzwerk, mit den Daten aus Vezeichnissen
die zusätzlich vorbereitete und erweiter werden.
"""

from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pickle
import os
from utils import *

DATADIR = "E:/Thomas/one-man-rps/data"

path = os.path.join(DATADIR, "images")

train_datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.2,
    horizontal_flip=True
)

valid_datagen = ImageDataGenerator()

train_generator = train_datagen.flow_from_directory(
    directory=path,
    target_size=IMG_NET_SIZE,
    color_mode="grayscale",
    batch_size=150,
    class_mode="sparse",
    shuffle=True,
    seed=42
)

valid_generator = valid_datagen.flow_from_directory(
    directory=path,
    target_size=IMG_NET_SIZE,
    color_mode="grayscale",
    batch_size=50,
    class_mode="sparse",
    shuffle=True,
    seed=100
)

model = create_model()

path = os.path.join(DATADIR, "logs")
tensorboard = keras.callbacks.TensorBoard(log_dir=path)
STEP_SIZE_TRAIN = train_generator.n // train_generator.batch_size
STEP_SIZE_VALID = valid_generator.n // valid_generator.batch_size

print("STEP_SIZE_TRAIN", STEP_SIZE_TRAIN, train_generator.n, train_generator.batch_size)
print("STEP_SIZE_VALID", STEP_SIZE_VALID, valid_generator.n, valid_generator.batch_size)

model.fit_generator(generator=train_generator,
                    steps_per_epoch=STEP_SIZE_TRAIN,
                    validation_data=valid_generator,
                    validation_steps=STEP_SIZE_VALID,
                    epochs=2,
                    callbacks=[tensorboard])

model.summary()
print("Trained model!")

save_model(DATADIR, model)
