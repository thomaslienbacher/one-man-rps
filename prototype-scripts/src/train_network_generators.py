"""
Dieses Script trainiert ein Neurales Netzwerk, mit den Bildern aus Vezeichnissen die vorher
mit split_train_valid.py getrennt wurden. Bei dieser Trainingsmethode werden die Bilder aus
den Verzeichnissen gelesen und gleichzeitig durch ImageDataGenerators verändert um künstlich
mehr verschiedene Bilder zu generieren. Zusätzlich werden Diagramme von Beispiel Bildern mittels
matplotlib erzeugt und auch gespeichert. Auch eine Statistik des Trainings wird so erzeugt und
gespeichert. ACHTUNG: Dateipfade sind hardcoded!
"""

import time
start_time = time.time()
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
from utils import *
import numpy as np
import pathlib
import matplotlib.pyplot as plt

DATADIR = "E:/Thomas/one-man-rps/data"

path = os.path.join(DATADIR, "images/train2")
path = pathlib.Path(path)
image_count = len(list(path.glob('*/*.jpg')))

BATCH_SIZE = 80
STEPS_PER_EPOCH = np.ceil(image_count / BATCH_SIZE)
CLASS_NAMES = np.array([item.name for item in path.glob('*')])
EPOCHS = 21
VIEW_EXAMPLES = True

print("Working in: ", DATADIR)
print("batch size", BATCH_SIZE)
print("epochs", EPOCHS)
print("steps per epoch", STEPS_PER_EPOCH)
print("class names", CLASS_NAMES)

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True
)

valid_datagen = ImageDataGenerator(
    rescale=1. / 255,
)

path = os.path.join(DATADIR, "images/train2")
train_generator = train_datagen.flow_from_directory(
    directory=path,
    target_size=IMG_NET_SIZE,
    color_mode="grayscale",
    batch_size=BATCH_SIZE,
    class_mode="sparse",
    shuffle=True,
)

path = os.path.join(DATADIR, "images/valid2")
valid_generator = valid_datagen.flow_from_directory(
    directory=path,
    target_size=IMG_NET_SIZE,
    color_mode="grayscale",
    batch_size=BATCH_SIZE,
    class_mode="sparse",
    shuffle=True,
)

if VIEW_EXAMPLES:
    sample_training_images, _ = next(train_generator)
    images_arr = sample_training_images[:16]
    fig, axes = plt.subplots(4, 4, figsize=(8, 8))
    axes = axes.flatten()

    for img, ax in zip(images_arr, axes):
        ax.imshow(img.reshape(IMG_NET_SIZE[0], IMG_NET_SIZE[1]), cmap="gray")
        ax.axis('off')
    plt.tight_layout()
    path = os.path.join(DATADIR, "examples_figure_" + time_escaped() + ".png")
    plt.savefig(path)
    plt.show()

model = create_model()

history = model.fit_generator(generator=train_generator,
                              steps_per_epoch=STEPS_PER_EPOCH,
                              validation_data=valid_generator,
                              validation_steps=STEPS_PER_EPOCH,
                              epochs=EPOCHS)

print("Trained model!")

model.summary()

acc = history.history["acc"]
val_acc = history.history["val_acc"]

loss = history.history["loss"]
val_loss = history.history["val_loss"]

epochs_range = range(EPOCHS)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label="Training Accuracy")
plt.plot(epochs_range, val_acc, label="Validation Accuracy")
plt.legend(loc="lower right")
plt.title("Training and Validation Accuracy")

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label="Training Loss")
plt.plot(epochs_range, val_loss, label="Validation Loss")
plt.legend(loc="upper right")
plt.title("Training and Validation Loss")
path = os.path.join(DATADIR, "training_statistics_" + time_escaped() + ".png")
plt.savefig(path)
plt.show()

save_model(DATADIR, model)

print("Execution took {} seconds".format(time.time() - start_time))
