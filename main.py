import textureHandler as th

import dearpygui.dearpygui as dpg
import array
import cv2 as cv
import numpy as np
import multiprocessing
from multiprocessing import Lock, Process, Queue, current_process, Event
# import queue
from time import sleep, time

dpg.create_context()
dpg.create_viewport(title='OpenCV Demo', width=800, height=600)
dpg.setup_dearpygui()

with dpg.texture_registry(show=False):
    dpg.add_raw_texture(th.frame_width, th.frame_height, th.texture_data, format=dpg.mvFormat_Float_rgb, tag='texture_tag', label='tex1')

with dpg.window(label='Image Tutorial'):
    dpg.add_image('texture_tag')


stop = Event()
imgIn = multiprocessing.Queue()
p = Process(target=th.collectData, args=(stop,imgIn,))
p.start()
dpg.show_viewport()

#####
# Replacing: dpg.start_dearpygui()
# with:
while dpg.is_dearpygui_running():
    if not imgIn.empty():
        print("Grabbed a frame")
        dpg.set_value('texture_tag', imgIn.get(block=False))
    # you can manually stop by using stop_dearpygui()
    else:
        # print("Queue is empty")
        sleep(0.5)
    dpg.render_dearpygui_frame()
###
print("stop.set()")
stop.set()
while not imgIn.empty():
    imgIn.get_nowait()
print("p.join()")
p.join()
print("destroy_context")
dpg.destroy_context()