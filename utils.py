import os
import random

import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import tensorflow.python.keras
from keras.api.models import Model
from keras.api.layers import Conv2D, Dense, Flatten, Input, Concatenate
from keras.api.optimizers import Adam
from keras.api.preprocessing.image import load_img, img_to_array
from sklearn.utils import shuffle
from sklearn.preprocessing import OneHotEncoder
from imgaug import augmenters
from typing import Tuple, List

column_image_center = 'Center'
column_steering = 'Steering'
column_steering_forward = 'Steering_forward'
column_steering_left = 'Steering_left'
column_steering_right = 'Steering_right'


def get_name_from_path(file_path: str) -> str:
    image_path_list = file_path.split('/')[-2:]
    image_path = os.path.join(image_path_list[0], image_path_list[1])
    return image_path


def import_data(directory_path: str) -> pd.DataFrame:
    columns = [column_image_center, column_steering]
    dataframe = pd.DataFrame()

    for value in range(0, 7):
        new_data = pd.read_csv(os.path.join(directory_path, f'log_{value}.csv'), names=columns)
        print(f'{value}:{new_data.shape[0]}', end='')

        new_data[column_image_center] = new_data[column_image_center].apply(get_name_from_path)
        dataframe = pd.concat([dataframe, new_data], ignore_index=True)

    print(f'total imported images {dataframe.shape[0]}')
    return dataframe


def encode_steering_data(data: pd.DataFrame) -> Tuple[List[str], np.ndarray]:
    encoder = OneHotEncoder(sparse_output=False)
    steering_encoded = encoder.fit_transform(data[[column_steering]])
    steering_labels = encoder.categories_[0]

    return steering_labels, steering_encoded


def balance_data(data: pd.DataFrame, display: bool) -> pd.DataFrame:
    steering_labels, steering_encoded = encode_steering_data(data)
    encoded_dataframe = pd.DataFrame(steering_encoded, columns=[f'Steering_{label}' for label in steering_labels])
    data = pd.concat([data.reset_index(drop=True), encoded_dataframe.reset_index(drop=True)], axis=1)

    if display:
        plt.figure(figsize=(10, 5))
        original_counts = data[column_steering].value_counts()
        original_counts.plot(kind='bar', width=0.5)
        plt.title('Original Data Distribution')
        plt.xlabel('Steering Command')
        plt.ylabel('Number of Samples')
        plt.show()

    samples_per_bin = 20
    remove_index_list = []

    for label in steering_labels:
        indices = data[data[column_steering] == label].index
        if len(indices) > samples_per_bin:
            indices = shuffle(indices)
            remove_index_list.extend(indices[samples_per_bin:])

    data.drop(remove_index_list, inplace=True)

    if display:
        plt.figure(figsize=(10, 5))
        balanced_counts = data[column_steering].value_counts()
        balanced_counts.plot(kind='bar', width=0.5)
        plt.title('Balanced Data Distribution')
        plt.xlabel('Steering Command')
        plt.ylabel('Number of Samples')
        plt.show()

    print(f'Removed Images: {len(remove_index_list)}')
    print(f'Remaining Images: {len(data)}')

    return data


def load_data(path: str, data: pd.DataFrame) -> tuple[np.ndarray, list[str], list[float], list[float], list[float]]:
    print(data.head())
    images_path: List[str] = []
    steering: List[str] = []
    steering_forward: List[float] = []
    steering_left: List[float] = []
    steering_right: List[float] = []

    for index in range(len(data)):
        index_data = data.iloc[index]
        images_path.append(os.path.join(path, index_data[column_image_center]))
        steering.append(index_data[column_steering])
        steering_forward.append(float(index_data[column_steering_forward]))
        steering_left.append(float(index_data[column_steering_left]))
        steering_right.append(float(index_data[column_steering_right]))

    images_paths = np.asarray(images_path)
    steering = np.asarray(steering)
    steering_forward = np.asarray(steering_forward)
    steering_left = np.asarray(steering_left)
    steering_right = np.asarray(steering_right)

    return images_paths, steering, steering_forward, steering_left, steering_right


def augment_image(image_path: str) -> np.ndarray:
    image = mpimg.imread(image_path)
    image = img_to_array(image)
    if np.random.rand() < 0.5:
        pan = augmenters.Affine(translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)})
        image = pan.augment_image(image)
    if np.random.rand() < 0.5:
        zoom = augmenters.Affine(scale=(1, 1.2))
        image = zoom.augment_image(image)
    if np.random.rand() < 0.5:
        brightness = augmenters.Multiply((0.5, 1.2))
        image = brightness.augment_image(image)
    # if np.random.rand() < 0.5:
    #     image = cv2.flip(image, 1)
    return image


def process_image_dimensions(image: np.ndarray) -> np.ndarray:
    image = image[54:120, :, :]
    image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
    image = cv2.GaussianBlur(image, (3, 3), 0)
    image = cv2.resize(image, (200, 66))
    image = image / 255.0
    return image


def create_model() -> Model:

    image_input = Input(shape=(66, 200, 3), name='image_input')
    x_input = Conv2D(24, (5, 5), strides=(2, 2), activation='relu')(image_input)
    x_input = Conv2D(36, (5, 5), strides=(2, 2), activation='relu')(x_input)
    x_input = Conv2D(48, (5, 5), strides=(2, 2), activation='relu')(x_input)
    x_input = Conv2D(64, (3, 3), activation='relu')(x_input)
    x_input = Conv2D(64, (3, 3), activation='relu')(x_input)

    x_input = Flatten()(x_input)
    x_input = Dense(100, activation='relu')(x_input)
    x_input = Dense(50, activation='relu')(x_input)
    x_input = Dense(10, activation='relu')(x_input)

    numerical_input = Input(shape=(3,), name='numerical_input')
    y_input = Dense(32, activation='relu')(numerical_input)
    y_input = Dense(16, activation='relu')(y_input)
    y_input = Dense(8, activation='relu')(y_input)

    combined_input = Concatenate()([x_input, y_input])
    z_output = Dense(50, activation='relu')(combined_input)
    z_output = Dense(10, activation='relu')(z_output)
    z_output = Dense(1, activation='linear')(z_output)

    model = Model(inputs=[image_input, numerical_input], outputs=z_output)
    model.compile(optimizer=Adam(learning_rate=0.0001), loss='mse')
    return model


def data_generator(images_path: str, steering: np.ndarray, steering_forward: np.ndarray,
                   steering_left: np.ndarray, steering_right: np.ndarray, batch_size: int, train_flag: bool):
    while True:
        batch_images = []
        batch_steering = []
        batch_steering_forward = []
        batch_steering_left = []
        batch_steering_right = []

        for i in range(batch_size):
            index = random.randint(0, len(images_path) - 1)
            if train_flag:
                image = augment_image(images_path[index])
            else:
                image = mpimg.imread(images_path[index])
                image = img_to_array(image)
        image = process_image_dimensions(image)
        batch_images.append(image)
        batch_steering.append(steering[index])
        batch_steering_forward.append(steering_forward[index])
        batch_steering_left.append(steering_left[index])
        batch_steering_right.append(steering_right[index])

        yield (
            [
                np.asarray(batch_images),
                np.column_stack((
                    batch_steering_forward,
                    batch_steering_left,
                    batch_steering_right))
            ],
            np.asarray(batch_steering)
        )





