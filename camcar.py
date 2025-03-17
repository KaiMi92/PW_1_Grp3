from basecar import *
from software.basisklassen import *
from software.basisklassen_cam import *
import pandas as pd 
import numpy as np
import cv2
import os
from datetime import datetime

class CamCar(BaseCar):
    def __init__(self) -> None:
        super().__init__()
        #self.cam = Camera(devicenumber: 0, buffersize: 1, skip_frame: 0, height: None, width: None, flip: True, colorspace:"bgr")
        self.cam = Camera()
    def __del__(self):
        """Releases camera and allows other processes to access it_"""
        print(f'del')
        self.cam.release()


    def get_img(self):
        i = self.cam.get_frame()
        self.save_img(i)
        return i

    def release(self) -> None:
        """Releases camera and allows other processes to access it_"""
        self.cam.release()

    def save_img(self, img):
        curr_time = datetime.now()
        timestr = curr_time.strftime('%Y-%m-%d_%H-%M-%S.%f')
        #timestr = time.strftime("%Y%m%d-%H%M%S%f")
        filename = './img/car_img_' + timestr + '.jpg'
        cv2.imwrite(filename, img)
        


 

    

    
