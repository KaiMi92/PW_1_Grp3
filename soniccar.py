from basecar import *
from software.basisklassen import *
import csv

fieldnames = ['Time','Distance','Direction','Speed','Steering']
setter_of_fieldnames = ['-','_distance','_direction','_speed','_steering_angle']

class SonicCar(BaseCar):

    def __init__(self):
        self._start_time = time.time()
        self._us = Ultrasonic() 
        self._csv_file = open('driving_data.csv', 'w', newline='')
        self._writer = csv.DictWriter( self._csv_file, fieldnames=fieldnames)
        self._writer.writeheader()  
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

    def __setattr__(self, name, value):
        # print(f"--> SonicCar setattr: set {name} to {value}")
        try:
            object.__setattr__(self, name, value)

            if name in setter_of_fieldnames:
                t = round(time.time() - self._start_time, 2)
                data = [{'Time': t, 'Distance': self._distance, 'Direction': self._direction, 'Speed': self._speed, 'Steering': self._steering_angle}]
                self._writer.writerows(data)
                print(f"Write CSV: {data}")
        except Exception as e:
            print(f"{__name__}: An exception occurred: {e}")
    