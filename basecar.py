from software.basisklassen import *

class basecar():
    def __init__(self, angle):
        self.steering_ang = angle

    def get_steering_angle(self):
        return self.steering_ang
    
    def set_steering_angle(self, angle):
        print(f'set angle to {angle}')

        fw = FrontWheels()        
        set_angle = fw.turn(angle)

        print(f'angle was set to {set_angle}')
        self.steering_ang = set_angle
        
        time.sleep(1)

    ''' steering angle of the car pi '''
    steering_angle = property(get_steering_angle, set_steering_angle)
