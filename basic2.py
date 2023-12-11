# -*- coding: utf-8 -*-
"""MIR_HF_basic2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cv8P2WZl7pIPqJuyCCDRodvM1ZyToqSb
"""

import os
import glob
import matplotlib.pyplot as plt
import cv2
import random
import numpy as np
import pickle
from mpl_toolkits.axes_grid1 import ImageGrid
import pathlib
import pandas as pd



import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow import keras
from tensorflow.keras import layers
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.models import Sequential
from keras.layers import GlobalAveragePooling2D
from tensorflow.keras.layers import Dense, Dropout

! pip install kaggle


! mkdir ~/.kaggle



! cp kaggle.json ~/.kaggle/



! chmod 600 ~/.kaggle/kaggle.json

! kaggle datasets download -d shawngano/gano-cat-breed-image-collection

! unzip gano-cat-breed-image-collection.zip

PATH = '/content/Gano-Cat-Breeds-V1_1'

def make_dataFrame(data):
    path=pathlib.Path(data)
    filepaths=list(path.glob(r"*/*.jpg"))
    labels=list(map(lambda x: os.path.split(os.path.split(x)[0])[1],filepaths))
    d1=pd.Series(filepaths,name='filepaths').astype(str)
    d2=pd.Series(labels,name='labels')
    df=pd.concat([d1,d2],axis=1)
    return df

dataFrame = make_dataFrame(PATH)

train_ratio = 0.75
test_ratio = 0.25

train, test = train_test_split(dataFrame, test_size = test_ratio, shuffle = True )

train_data_generator=ImageDataGenerator(
    rescale = 1./255,
    horizontal_flip=True,
    rotation_range=20,
    width_shift_range=.2,
    height_shift_range=.2,
    zoom_range=.2,
    shear_range=.2,
    fill_mode="nearest",
    validation_split=.2)

test_data_generator = ImageDataGenerator(rescale = 1./255)

BATCH_SIZE = 16
IMG_SIZE = (350, 350)

train_generator = train_data_generator.flow_from_dataframe(
    dataframe = train,
    x_col = "filepaths",
    y_col = "labels",
    target_size = IMG_SIZE,
    batch_size = BATCH_SIZE,
    class_mode = "categorical",
    subset = 'training',
    color_mode='rgb',
    shuffle = True,
    seed = 22
)

valid_generator = train_data_generator.flow_from_dataframe(
    dataframe = train,
    x_col = "filepaths",
    y_col = "labels",
    target_size = IMG_SIZE,
    batch_size = BATCH_SIZE,
    class_mode = "categorical",
    subset = 'validation',
    color_mode='rgb',
    shuffle = True,
    seed = 22
)

test_generator = test_data_generator.flow_from_dataframe(
    dataframe = test,
    x_col = "filepaths",
    target_size = IMG_SIZE,
    batch_size = 1,
    color_mode='rgb',
    class_mode = None,
    shuffle = False
)

model = keras.Sequential(
    [
        layers.Conv2D(32, (4,4), activation='relu', input_shape=(350,350,3)),
        layers.Conv2D(32, (4,4), activation='relu', padding='same'),
        layers.Conv2D(128, (4,4), activation='relu', padding='same'),
        layers.Conv2D(128, (4,4), activation='relu', padding='same'),
        layers.MaxPooling2D(2, 2),
        layers.Dropout(.3),

        layers.Conv2D(256, (4,4), activation='relu', padding='same'),
        layers.Conv2D(256, (4,4), activation='relu', padding='same'),
        layers.Conv2D(128, (4,4), activation='relu', padding='same'),
        layers.Conv2D(128, (4,4), activation='relu', padding='same'),
        layers.MaxPooling2D(2, 2),
        layers.Dropout(.3),

        layers.MaxPooling2D(2, 2),
        layers.Dense(1024, activation='relu'),
        layers.Dense(512, activation='relu'),
        layers.Dropout(.3),
        layers.Flatten(),
        layers.Dense(32, activation='relu'),

        layers.Dense(15, activation='softmax')
    ]
)

model.summary()

model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), metrics=["accuracy"])

history = model.fit(
    train_generator,
    steps_per_epoch = train_generator.n//train_generator.batch_size,
    validation_data = train_generator,
    validation_steps = valid_generator.n//valid_generator.batch_size,
    epochs = 5)

score = model.evaluate_generator(valid_generator)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

predict=model.predict_generator(test_generator, steps = len(test_generator.filenames))

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(25)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()