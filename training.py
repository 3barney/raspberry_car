import pandas as pd

print('Setting UP')
import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from sklearn.model_selection import train_test_split
from utils import *

steering_mapping = {'forward': 0, 'left': 1, 'right': 2}
image_data_directory = 'data_collected'

image_dataframe = import_data(image_data_directory)
print(image_dataframe.head())

image_dataframe = balance_data(image_dataframe, display=True)  # vis and balance

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
# y = data_frame['steering']
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

print("DATA FRAME TYPES")
print(data_frame.dtypes)
print("DATA FRAME TYPES END ----------------------------")

# data generators (training and validation)
train_generator = data_generator(
    xTrain['images_path'].values,
    xTrain['steering_forward'].values,
    xTrain['steering_left'].values,
    xTrain['steering_right'].values,
    batch_size=32,
    train_flag=True
)

val_generator = data_generator(
    xVal['images_path'].values,
    xVal['steering_forward'].values,
    xVal['steering_left'].values,
    xVal['steering_right'].values,
    batch_size=32,
    train_flag=False
)

# model
model = create_model()
print(model.summary())

# train
history = model.fit(
    train_generator,
    steps_per_epoch=len(xTrain) // 32,
    epochs=10,
    validation_data=val_generator,
    validation_steps=len(xVal) // 32
)

# save model
model.save('model.h5')
print('Model Saved')


#results
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['Training', 'Validation'])
plt.title('Loss')
plt.xlabel('Epoch')
plt.show()


