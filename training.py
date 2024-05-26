import pandas as pd

print('Setting UP')
import os

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from sklearn.model_selection import train_test_split
from utils import *

batch_data_size = 5  # 32
steering_mapping = {'forward': 0, 'left': 1, 'right': 2}
image_data_directory = 'data_collected'

image_dataframe = import_data(image_data_directory)
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

val_generator = tf.data.Dataset.from_generator(
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

# train
history = model.fit(
    train_generator,
    steps_per_epoch=len(xTrain) // batch_data_size,
    epochs=10,
    validation_data=val_generator,
    validation_steps=len(xVal) // batch_data_size
)

# save model
model.save('model.keras')
print('Model Saved')


#results
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['Training', 'Validation'])
plt.title('Loss')
plt.xlabel('Epoch')
plt.show()

# Evaluate model
test_loss, test_mae, test_mse = model.evaluate(val_generator, steps=len(xVal) // batch_data_size)
print(f'Test Loss: {test_loss}')
print(f'Test MAE: {test_mae}')
print(f'Test MSE: {test_mse}')


# Plot additional metrics
plt.plot(history.history['mae'])
plt.plot(history.history['val_mae'])
plt.legend(['Training MAE', 'Validation MAE'])
plt.title('Mean Absolute Error')
plt.xlabel('Epoch')
plt.show()


plt.plot(history.history['mse'])
plt.plot(history.history['val_mse'])
plt.legend(['Training MSE', 'Validation MSE'])
plt.title('Mean Squared Error')
plt.xlabel('Epoch')
plt.show()

