import pandas as pd

print('Setting UP')
import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from sklearn.model_selection import train_test_split
from utils import *


image_data_path = 'data_collected'
image_dataframe = import_data(image_data_path)
print(image_dataframe.head())

image_dataframe = balance_data(image_dataframe, display=True)  # vis and balance

# preprocess
images_path, steering, steering_forward, steering_left, steering_right = load_data(image_data_path, image_dataframe)
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
y = data_frame['steering']

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





# augment_data

#### STEP 5 - AUGMENT DATA

#### STEP 6 - PREPROCESS

#### STEP 7 - CREATE MODEL
model = createModel()

#### STEP 8 - TRAINNING
history = model.fit(dataGen(xTrain, yTrain, 100, 1),
                                  steps_per_epoch=100,
                                  epochs=10,
                                  validation_data=dataGen(xVal, yVal, 50, 0),
                                  validation_steps=50)

#### STEP 9 - SAVE THE MODEL
model.save('model.h5')
print('Model Saved')

#### STEP 10 - PLOT THE RESULTS
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['Training', 'Validation'])
plt.title('Loss')
plt.xlabel('Epoch')
plt.show()


