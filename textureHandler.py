import cv2 as cv
import numpy as np
import dearpygui.dearpygui as dpg
from multiprocessing import Queue
from time import time, sleep

# imgOut = Queue()
# runProcess = True

webcam = cv.VideoCapture(0)

ret, frame = webcam.read()
frame_width = webcam.get(cv.CAP_PROP_FRAME_WIDTH)
frame_height = webcam.get(cv.CAP_PROP_FRAME_HEIGHT)
video_fps = webcam.get(cv.CAP_PROP_FPS)

# print("Input Data")
# print(type(frame))
# print("Dim:", frame.ndim)
# print("Shape:", frame.shape)
# print("Size:", frame.size)
# print("Stores type:", frame.dtype)

data = np.flip(frame, 2) # BGR -> RGB
data = data.ravel() # flatten
data = np.asfarray(data, dtype='f') # change data to 32bit floats
texture_data = np.true_divide(data, 255.0) # normalize data

# print("Texture Data")
# print(type(texture_data))
# print("Dim:", texture_data.ndim)
# print("Shape:", texture_data.shape)
# print("Size:", texture_data.size)
# print("Stores type:", texture_data.dtype)

def collectData(stop, imgIn):
    print("Beginning data collection")
    while not stop.is_set():
        # print("Test")
        # sleep(0.5)
        print("Pushing a frame")
        ret, frame = webcam.read()
        data = np.flip(frame, 2) # BGR -> RGB
        data = data.ravel() # flatten
        data = np.asfarray(data, dtype='f') # change data to 32bit floats
        imgIn.put(np.true_divide(data, 255.0), block=False) # normalize data
        print("Pushed a frame")
        # getFrameAsTexture(imgIn)
    webcam.release()

# def getFrameAsTexture(imgIn):
#     print("Pushing a frame")
#     ret, frame = webcam.read()
#     data = np.flip(frame, 2) # BGR -> RGB
#     data = data.ravel() # flatten
#     data = np.asfarray(data, dtype='f') # change data to 32bit floats
#     imgIn.put(np.true_divide(data, 255.0)) # normalize data
#     # texture_data = imgOut.put(np.true_divide(data, 255.0)) # normalize data
