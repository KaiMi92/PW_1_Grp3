from software.basisklassen import *
import os

class BaseCar:

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
        self._direction = 0
        self._steering_angle = 90
        self._speed = 0

    # def __setattr__(self, name, value):
    #     print(f"--> BaseCar setattr: set {name} to {value}")
    #     object.__setattr__(self, name, value)
        
    ''' getter-method of steering angle'''
    @property
    def steering_angle(self):
        return self._steering_angle
    
    ''' setter-method of steering angle'''
    @steering_angle.setter
    def steering_angle(self, angle):
        if self._steering_angle == angle:
            return
        
        set_angle = self._fw.turn(angle)
        self._steering_angle = set_angle        
        time.sleep(0.1)

    ''' getter-method of speed'''
    @property
    def speed(self):
        return self._speed
    
    ''' setter-method of speed'''
    @speed.setter
    def speed(self, speed):
        if self._speed == speed:
            return
        
        # Limit parameter values
        if speed < -100:
            self._speed = -100
            print(f'speed was set to {self._speed}')
        elif speed > 100:
            self._speed = 100
            print(f'speed was set to {self._speed}')
        else:
            self._speed = speed

        # calculate direction
        if self._speed < 0:
            if self._direction != -1:
                self._direction = -1
        elif self._speed > 0:
            if self._direction != 1:
                self._direction = 1
        else:
            if self._direction != 0:
                self._direction = 0

        self._bw.speed = abs(self._speed)

    ''' getter-method of direction'''
    @property   
    def direction(self):
        return self._direction

    def drive(self, speed=None, steering_angle=None):
        if self._speed == speed and self._steering_angle == steering_angle:
            # needed values already set
            # nothing to do
            return
        
        drctn = self._direction
        
        # set steering angle before start driving        
        if not steering_angle is None:
            self.steering_angle = steering_angle

        # set speed and start driving
        if not speed is None:
            self.speed = speed

        if drctn != self._direction:
            if self.direction == 1:
                print(f'Drive Forward with speed {self._speed}')
                self._bw.forward()
            elif self.direction == -1:
                print(f'Drive Backward with speed {self._speed}')
                self._bw.backward()
            else:
                print(f'Stop Driving with speed {self._speed}')
                self._bw.stop()

    def stop(self):
        self.drive(0,90)