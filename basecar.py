from software.basisklassen import *

class Auto:
    def __init__(self):
        self._fw = FrontWheels()        
        self._bw = BackWheels()
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
        
        self._bw.speed = abs(self._speed)
        return self._speed
    
    @property
    def direction(self):
        if self._speed <0:
            return -1
        if self._speed >0:
            return 1
        else:
            return 0

    def drive(self, steering_angle, speed, direction):
        if steering_angle is None:
            self._steering_angle = 90
        if speed is None:
            self._speed = 0
        if direction is None:
            self._direction = 0
        else:
            self._steering_angle = steering_angle
            self._speed = speed
            self._direction = direction
        if self.direction == 1:
            self._bw.forward()
        if self.direction == -1:
            self._bw.backward()
        if self.direction == 0:
            self._bw.stop()

    def stop(self):
        self.drive(0)
        