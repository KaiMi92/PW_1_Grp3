from basecar import *
from software.basisklassen import *
import csv

class SonicCar(BaseCar):

    def __init__(self):
        self._us = Ultrasonic() 
        self._distance = 0
        self._distance = self.get_distance()
        super().__init__()

    ''' getter-method of distance'''
    @property   
    def distance(self):
        return self._distance

    ''' setter-method of distance'''
    @distance.setter
    def distance(self, d):
        self._distance = d

    def get_distance(self):
        #self._us.distance()
        d = self._us.distance()
        if d != self._distance:
            self._distance = self._us.distance()
        return self._distance

    