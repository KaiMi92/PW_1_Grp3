"""Implementation in the Soniccar file

The aim of this class is to complement the Sonsorcar class with the functions of distance sensors. 
Soniccar should be available as a class later for other driving modes from projectphase 1 
and make the other classes usable, e.g. Basecar.

author: Team 3 / Gen 8
"""
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

    