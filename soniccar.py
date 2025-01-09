from basecar import *
from software.basisklassen import *

class SonicCar(BaseCar):
    def __init__(self):
        self._us = Ultrasonic()   
        super().__init__()


    def get_distance(self):
        #self._us.distance()
        d = self._us.distance()
        print(f'd = {d}')
        return d
    