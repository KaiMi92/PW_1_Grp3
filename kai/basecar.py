from software.basisklassen import *

class Auto:
    def __init__(self):
        self._steering_angle = 0
        self._direction = 0
        self._speed = 0

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
        return self._steering_angle


    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, new_speed):
        if new_speed < 0 and new_speed > 100:
            print ("Geschwindigkeit außerhalb des möglichen")
        
        if new_speed < 0:
            self._speed = 0
            print("Setze Geschwindigkeit auf 0")
        
        if new_speed > 100:
            self._speed = 100
            print("Setze Geschwindigkeit auf 100")
        return self._speed