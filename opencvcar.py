import cv2
import numpy as np
from processor import Processor
from camcar import CamCar
import math
import time
import calc_steering_angle_1
import calc_steering_angle_2
import calc_steering_angle_3
import calc_steering_angle_4
import calc_steering_angle_5

methodDictionary = {1: calc_steering_angle_1.calculate_steering_angle, 
                    2: calc_steering_angle_2.calculate_steering_angle,
                    3: calc_steering_angle_3.calculate_steering_angle,
                    4: calc_steering_angle_4.calculate_steering_angle,
                    5: calc_steering_angle_5.calculate_steering_angle}

# Setzen der Konstantwerte für Geschwindigkeit und Lenkwinkel Geradeaus, maximal Links und maximal rechts
SPEED = 35
STRAIGHT_FORWARD = 90
MAX_TURN_LEFT = 45
MAX_TURN_RIGHT = 135

class OpenCvCar(CamCar):

    def __init__(self):
        #BaseCar.fieldnames_to_log = BaseCar.fieldnames_to_log + ["distance"]
        #BaseCar.csv_col_name_of_fieldnames = BaseCar.csv_col_name_of_fieldnames + ["Distance"]
        super().__init__()
        self._prev_frame_time = time.time() 
        self._new_frame_time = time.time()
        self._proc = Processor()
        self.speed = 0
        self.steering_angle = STRAIGHT_FORWARD

    ''' Image processor '''
    @property   
    def proc(self):
        return self._proc

    def start_driving(self):
          # start driving (and steering)
        try:  
            self.drive(speed = SPEED, steering_angle = STRAIGHT_FORWARD)      
        except Exception as e:
            print(f"An exception occurred: {e}")
            self.stop()
        finally:
            print("Everything ok!")
            self.stop()

    def stop_driving(self):
        self.stop()

    def generate_stream(self):
        while True:
            # print("============================================")
            # print(f"Verwende Methode {self._proc.calc_angle_method}")

            # frame = camera_instance.get_frame()
            frame = self.get_img()
            line_filter, lines = self._proc.line_filter(frame)
            # steering_angle = calc_steering_angle.calculate_steering_angle(line_filter, lines)   # einzeichnen im bild?

            method = methodDictionary[self._proc.calc_angle_method]
            angle = method(line_filter, lines)
            if self.speed > 0:
                self.steering_angle = angle

            self.draw_steering_angle(line_filter, angle)
            self.draw_fps(line_filter)

            # filtered = proc.filter_color(frame)
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # canny = cv2.Canny(gray, 100, 200)
            stacked = np.hstack([line_filter]) # canny, filtered])
            _, x = cv2.imencode(".jpeg", stacked)
            x_bytes = x.tobytes()

            x_string = (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + x_bytes + b'\r\n\r\n')
            
            yield x_string        

        
    def draw_fps(self, image):
        global prev_frame_time
        global new_frame_time

        # Calculating True FPS
        self._new_frame_time = time.time()
        fps = 1 / (self._new_frame_time - self._prev_frame_time)
        self._prev_frame_time = self._new_frame_time

        text = str(round(fps,1)) + " fps"
        position  =(10,40)
        font = cv2.FONT_HERSHEY_SIMPLEX 
        fontscale = 0.5
        color = (0,0,255) # Hier im BGR-Modus + Werte vom Type 'unit8'
        thickness = 2
        linestyle = 1
        img_text = cv2.putText(image, text, position,font, fontscale, color, thickness, linestyle)

    

    def draw_steering_angle(self, image, steering_angle):
        height, width, channels = image.shape
        angle = steering_angle - 90

        x = height * math.tan(math.radians(angle))
        x45 = height * math.tan(math.radians(45))
        x135 = height * math.tan(math.radians(135))

        middle = int((width - 1) / 2)
        x1 = middle
        y1 = height - 1
        x2 = middle + int(x)
        y2 = 0
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.line(image, (x1, y1), (middle + int(x45), y2), (255, 255, 255), 2)
        cv2.line(image, (x1, y1), (middle + int(x135), y2), (255, 255, 255), 2)
        # print(f'steering_angle = {steering_angle}, angle = {angle}, x = {x}, P1({x1}|{y1}), P2({x2}|{y2}) ')
