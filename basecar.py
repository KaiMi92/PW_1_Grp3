from software.basisklassen import *

UNDEFINED = -1000

class BaseCar:

    def __init__(self):
        self._steering_angle = 90
        self._speed = 0
        self._direction = 0
        self._fw = FrontWheels()        
        self._bw = BackWheels()
        self._bw.stop()

    ''' getter-method of steering angle'''
    @property
    def steering_angle(self):
        return self._steering_angle
    
    ''' setter-method of steering angle'''
    @steering_angle.setter
    def steering_angle(self, angle):
        print(f'set angle to {angle}')

        set_angle = self._fw.turn(angle)

        print(f'angle was set to {set_angle}')
        self._steering_angle = set_angle
        
        time.sleep(1)

    ''' getter-method of speed'''
    @property
    def speed(self):
        return self._speed
    
    ''' setter-method of speed'''
    @speed.setter
    def speed(self, speed):
        print(f'speed to {speed}')

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
            self._direction = -1
        elif self._speed > 0:
            self._direction = 1
        else:
            self._direction = 0

        self._bw.speed = abs(self._speed)

    ''' getter-method of direction'''
    @property   
    def direction(self):
        return self._direction

    def drive(self, speed=None, steering_angle=None):
        # set steering angle before start driving
        if steering_angle:
            self.steering_angle = steering_angle

        # set speed and start driving
        if speed:
            self.speed = speed

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
        self._bw.stop()

