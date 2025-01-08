from software.basisklassen import *

class basecar:
    def __init__(self):
        self._steering_angle = 90
        self._speed = 0
        #self._direction = 0

    ''' getter-method of steering angle'''
    def get_steering_angle(self):
        return self._steering_angle
    
    ''' setter-method of steering angle'''
    def set_steering_angle(self, angle):
        print(f'set angle to {angle}')

        fw = FrontWheels()        
        set_angle = fw.turn(angle)

        print(f'angle was set to {set_angle}')
        self._steering_angle = set_angle
        
        time.sleep(1)

    ''' steering angle of the car pi '''
    steering_angle = property(get_steering_angle, set_steering_angle)

    ''' getter-method of speed'''
    def get_speed(self):
        return self._speed
    
    ''' setter-method of speed'''
    def set_speed(self, speed):
        print(f'speed to {speed}')
        if speed < -100:
            speed = -100
            print(f'speed was set to {speed}')
        if speed > 100:
            speed = 100
            print(f'speed was set to {speed}')
        #bw = BackWheels()

        #bw.speed = speed
        self._speed = speed
        #return self._speed

    ''' speed of the car pi '''
    speed = property(get_speed, set_speed)

    ''' getter-method of direction'''
    @property   
    def direction(self):
        if self._speed < 0:
            return -1
        elif self._speed > 0:
            return 1
        else: 
            return 0

    
