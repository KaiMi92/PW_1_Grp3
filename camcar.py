from basecar import *
from software.basisklassen import *
from software.basisklassen_cam import *
import pandas as pd 
import numpy as np
import cv2
from datetime import datetime


class CamCar(BaseCar):

    def __init__(self) -> None:
        super().__init__()
        self._cam = Camera()

    def __del__(self):
        """ Releases camera and allows other processes to access it_"""
        print(f'del')
        self._cam.release()

    @property   
    def cam(self):
        """ Camera reference """
        return self._cam


    def get_img(self):
        i = self._cam.get_frame()
        # self.save_img(i)
        return i

    def release(self) -> None:
        """Releases camera and allows other processes to access it_"""
        self._cam.release()

    def save_img(self, img, suffix):
        curr_time = datetime.now()
        timestr = curr_time.strftime('%Y-%m-%d_%H-%M-%S.%f')
        #timestr = time.strftime("%Y%m%d-%H%M%S%f")
        filename = './img/car_img_' + timestr + '_' + str(suffix) + '.jpg'
        cv2.imwrite(filename, img)
