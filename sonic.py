from basecar import *
from software.basisklassen import *

class SonicCar(Auto):
    def __init__(self):
        super().__init__()
        self._us = Ultrasonic()

    def get_sonic(self):
        s = self._us.distance()
        return s