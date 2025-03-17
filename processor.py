import cv2
import numpy as np

class Processor():
    def __init__(self):
        self.lower_hue = 0
        self.lower_value = 0
        self.lower_saturation = 0

        self.upper_hue = 180
        self.upper_value = 180
        self.upper_saturation = 180

    def filter_color(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([self.lower_hue, self.lower_saturation, self.lower_value])
        upper = np.array([self.upper_hue, self.upper_saturation, self.upper_value])
        filtered = cv2.inRange(hsv, lower, upper)
        return filtered


        
        