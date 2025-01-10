from software.basisklassen import *
import os

class Auto:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'software/config.json')
        turning_offset = 0
        forward_A = 0
        forward_B = 0
        try:
            with open(filename, "r") as config_file:
                json_data = json.load(config_file)
                turning_offset = json_data["turning_offset"]
                forward_A = json_data["forward_A"]
                forward_B = json_data["forward_B"]
                print(f"Using car params: turning_offset = {turning_offset}, forward_A = {forward_A}, forward_B = {forward_B}")
        except Exception as e:
            print("Error reading config file: ", e)

        self._fw = FrontWheels(turning_offset=turning_offset)        
        self._bw = BackWheels(forward_A=forward_A, forward_B=forward_B)
        self._bw.stop()
        self._steering_angle = 90
        self._speed = 0
        self._direction = 0

    @property
    def steering_angle(self):
        return self._steering_angle
    
    @steering_angle.setter
    def steering_angle(self, new_angle):
        if new_angle < 45 and new_angle > 135:
            print ("Du kannst das Lenkrad nicht weiter drehen")

        if new_angle < 45:
            print("Setze den Lenkwinkel auf 45")
            self._steering_angle = 45 

        if new_angle > 135:
            print("Setze den Lenkwinkel auf 135")
            self._steering_angle = 135
        else:
            self._steering_angle = new_angle
        
        self._fw.turn(self._steering_angle)
        return self._steering_angle


    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, new_speed):
        if new_speed < 0 and new_speed >= -100:
            self._speed = new_speed
            print("Rückwärtsfahrt")

        if new_speed > 0 and new_speed <= 100:
            self._speed = new_speed
            print("Vorwärtsfahrt")

        if self._speed <0:
            self._direction = -1
        elif self._speed >0:
            self._direction = 1
        else:
            self._direction = 0


        self._bw.speed = abs(self._speed)
        return self._speed
    
    @property
    def direction(self):
        return self._direction

    def drive(self, steering_angle=None, speed=None):
        if not steering_angle is None:
            self.steering_angle = steering_angle
        if not speed is None:
            self.speed = speed

        if self.direction == 1:
            self._bw.forward()
        elif self.direction == -1:
            self._bw.backward()
        else:
            self._bw.stop()

    def stop(self):
        self._bw.stop()
        self._steering_angle = 90
