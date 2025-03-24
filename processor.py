import cv2
import numpy as np

class Processor():
    def __init__(self):
        self.lower_hue = 95
        self.lower_saturation = 80
        self.lower_value = 50

        self.upper_hue = 130
        self.upper_saturation = 255
        self.upper_value = 255

        self.calc_angle_method = 2
        self.use_average = False

    def filter_color(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([self.lower_hue, self.lower_saturation, self.lower_value])
        upper = np.array([self.upper_hue, self.upper_saturation, self.upper_value])
        filtered = cv2.inRange(hsv, lower, upper)
        filtered = cv2.cvtColor(filtered, cv2.COLOR_GRAY2BGR)
        return filtered

    def line_filter(self, img):
        
        img_crop = img[150:350,:,:]

        # Parkettfugen wurden als Linien erkannt
        # daher erst MedianBlur, um Fugen zu verwischen
        # img_crop = cv2.medianBlur(img_crop,7)
        img_blur = cv2.blur(img_crop,(5, 5))

        img_hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([self.lower_hue, self.lower_saturation, self.lower_value])
        upper_blue = np.array([self.upper_hue, self.upper_saturation, self.upper_value])
        mask = cv2.inRange(img_hsv, lower_blue, upper_blue)

        edges = cv2.Canny(mask, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=30, minLineLength=30, maxLineGap=20)

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(img_crop, (x1, y1), (x2, y2), (0, 255, 0), 2)

        return img_crop, lines

        