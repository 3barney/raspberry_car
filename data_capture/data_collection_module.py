import os
import cv2
import time
import pandas as pd

from datetime import datetime
from picamera2 import Picamera2, Preview

global imageList, turnList
folderCount = 0
count = 0
imageList = []
turnList = []

data_collected_directory = os.path.join(os.getcwd(), 'data_collected')

while os.path.exists(os.path.join(data_collected_directory, f'IMG{str(folderCount)}')):
    folderCount += 1

new_data_collected_directory = data_collected_directory + "/IMG" + str(folderCount)
os.makedirs(new_data_collected_directory)


def saveData(image, turn):
    global imageList, turnList
    timestamp = str(datetime.timestamp(datetime.now())).replace('.', '')
    file_name = os.path.join(new_data_collected_directory, f'Image_{timestamp}.jpg')
    cv2.imwrite(file_name, image)
    imageList.append(file_name)
    turnList.append(turn)


def saveLog():
    global imageList, turnList
    print(f"About to save  images: {len(imageList)} turns: {len(turnList)}")
    raw_data = {'Image': imageList, 'Turn': turnList}
    data_frame = pd.DataFrame(raw_data)
    data_frame.to_csv(os.path.join(data_collected_directory, f'log_{str(folderCount)}.csv'), index=False, header=False)
    print(f'log saved ::: total_images {len(imageList)}')


if __name__ == '__main__':
    picam2 = Picamera2()
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    time.sleep(2)  # start camera

    for _ in range(10):
        img = picam2.capture_array()
        saveData(img, "forward")
        time.sleep(1)

    picam2.stop_preview()
    picam2.close()
    saveLog()
