from software.basisklassen import *

class basecar:
    def __init__(self, angle):
        self._steering_angle = angle

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
        if speed < 0:
            speed = 0
        if speed > 100:
            speed = 100
        bw = BackWheels()

        bw.speed = speed
        self._speed = speed
        #return self._speed

    ''' speed of the car pi '''
    speed = property(get_speed, set_speed)