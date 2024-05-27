import pandas as pd

print('Setting UP')
import os

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight
from tensorflow.python.keras.callbacks import EarlyStopping
from utils import *

batch_data_size = 32  # 32
steering_mapping = {'forward': 0, 'left': 1, 'right': 2}
image_data_directory = 'data_collected'

image_dataframe = import_data(image_data_directory)
print(image_dataframe.shape)
print(image_dataframe.head())

image_dataframe = balance_data(image_dataframe, display=True)  # vis and balance
print(image_dataframe.head())

# preprocess
images_path, steering, steering_forward, steering_left, steering_right = load_data(
    image_data_directory,
    image_dataframe)

print(f' image_path :: {len(images_path)} steering :: {len(steering)} steering_forward :: {len(steering_forward)} '
      f'steering_left :: {len(steering_left)} steering_right {len(steering_right)}')

# cv2.imshow('Test Image',cv2.imread(images_path[5]))
# cv2.waitKey(0)


# split: validation and train setup
data_frame = pd.DataFrame({
      'images_path': images_path,
      'steering': steering,
      'steering_forward': steering_forward,
      'steering_left': steering_left,
      'steering_right': steering_right
})

X = data_frame[['images_path', 'steering_forward', 'steering_left', 'steering_right']]
y = data_frame[['steering_forward', 'steering_left', 'steering_right']]

print(X.head())
print(y.head())

xTrain, xVal, yTrain, yVal = train_test_split(
      X,
      y,
      test_size=0.2,
      random_state=10
)

print(f'total training Images: {len(xTrain)}')
print(f'total validation Images: {len(xVal)}')

# data generators (training and validation)
train_generator = tf.data.Dataset.from_generator(
    lambda: data_generator(
        xTrain['images_path'].values,
        xTrain['steering_forward'].values,
        xTrain['steering_left'].values,
        xTrain['steering_right'].values,
        batch_size=batch_data_size,
        train_flag=True
    ),
    output_signature=(
        {
            'image_input': tf.TensorSpec(shape=(None, 66, 200, 3), dtype=tf.float32),
            'numerical_input': tf.TensorSpec(shape=(None, 3), dtype=tf.float32)
        },
        tf.TensorSpec(shape=(None, 3), dtype=tf.float32)
    )
)

validation_generator = tf.data.Dataset.from_generator(
    lambda: data_generator(
        xVal['images_path'].values,
        xVal['steering_forward'].values,
        xVal['steering_left'].values,
        xVal['steering_right'].values,
        batch_size=batch_data_size,
        train_flag=False
    ),
    output_signature=(
        {
            'image_input': tf.TensorSpec(shape=(None, 66, 200, 3), dtype=tf.float32),
            'numerical_input': tf.TensorSpec(shape=(None, 3), dtype=tf.float32)
        },
        tf.TensorSpec(shape=(None, 3), dtype=tf.float32)
    )
)

# model
model = create_model()
print(model.summary())

# we have more forwards
class_weights = class_weight.compute_class_weight(
    class_weight='balanced',
    classes=np.unique(np.argmax(yTrain, axis=1)),
    y=np.argmax(yTrain, axis=1)
)
class_weights_dictionary = {i: class_weights[i] for i in range(len(class_weights))}
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# train
history = model.fit(
    train_generator,
    steps_per_epoch=len(xTrain) // batch_data_size,
    epochs=10,
    validation_data=validation_generator,
    validation_steps=len(xVal) // batch_data_size,
    # class_weight=class_weights_dictionary,
    # callbacks=[early_stopping]
)

# save model
model.save('model.keras')
print('Model Saved')


# results
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['Training', 'Validation'])
plt.title('Loss')
plt.xlabel('Epoch')
plt.show()

# Evaluate model
test_loss, test_accuracy = model.evaluate(validation_generator, steps=len(xVal) // batch_data_size)
# test_loss, test_mae, test_mse = model.evaluate(validation_generator, steps=len(xVal) // batch_data_size)
print(f'Test Loss: {test_loss}')
print(f'Test accuracy: {test_accuracy}')
# print(f'Test MAE: {test_mae}')
# print(f'Test MSE: {test_mse}')
#
# # Plot additional metrics
# plt.plot(history.history['mae'])
# plt.plot(history.history['val_mae'])
# plt.legend(['Training MAE', 'Validation MAE'])
# plt.title('Mean Absolute Error')
# plt.xlabel('Epoch')
# plt.show()
#
#
# plt.plot(history.history['mse'])
# plt.plot(history.history['val_mse'])
# plt.legend(['Training MSE', 'Validation MSE'])
# plt.title('Mean Squared Error')
# plt.xlabel('Epoch')
# plt.show()


# Test model

for j in range(0, 10):
    images_path_0 = data_frame.iloc[j]['images_path']
    steering_0 = data_frame.iloc[j]['steering']
    steering_forward_0 = data_frame.iloc[j]['steering_forward']
    steering_left_0 = data_frame.iloc[j]['steering_left']
    steering_right_0 = data_frame.iloc[j]['steering_right']

    prediction = test_model(model, images_path_0, steering_0,
                            steering_forward_0, steering_left_0, steering_right_0)
    print(f'image {images_path_0} Recorded vs Prediction : {steering_0} : {prediction}')


# converter = tf.lite.TFLiteConverter.from_keras_model()
#
