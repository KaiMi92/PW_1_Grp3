from basecar import *
from software.basisklassen import *
import csv

fieldnames = ['Time','Distance','Direction','Speed','Steering','IR-v1','IR-v2','IR-v3','IR-v4','IR-v5']
setter_of_fieldnames = ['-','_distance','_direction','_speed','_steering_angle', '_ir_values']

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

    