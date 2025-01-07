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
