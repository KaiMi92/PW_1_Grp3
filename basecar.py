"""BaseCar implementation
 
implements the requirements of Code2Camp project phase 1

author: Team 3 / Gen 8
"""
from software.basisklassen import *
import os
import csv

class BaseCar:
    """
    A class to represent a car with basic attribute like speed or steering_angle.

    Attributes
    ----------
    speed : int
        speed of the car in percent
            valid values are 0 .. 100
    steering_angle : int
        steering angle of the car in degrees.
            90 degrees means straight forward
            max. left steering angle is 135
            max. right steering angle is 45
    direction : int
        direction of the car with the following values
            0: no direction because car is not moving
            1: car is moving forward
            -1: car is moving backward

    Methods
    -------
    drive(speed=None, steering_angle=None):
        start moving the car with the given parameters
        if the values of a paramter is empty the internal values will be used
    stop():
        start moving the car with the given parameters
    """

    
    finished = False
    """
        class variable to stop the car
    """
    
    fieldnames_to_log = ['direction','speed','steering_angle']
    """
        class attribute: name of all setters which values should logged to file
    """

    csv_col_name_of_fieldnames = ['Direction','Speed','Steering']
    """
        class attribute: name of the csv-columns of all setters which values should logged to file
    """

    def __init__(self, log_filename="car_log.csv"):
        """Constructor method.

        The Contructor reads the config file to set individual car parameters for the 
        instantiation of the classes for the front- and the backwheels.
        Also default values are set for all attributes.
        """

        # Interne Attribute direkt setzen, ohne wieder __setattr__ aufzurufen,
        # damit wir keine Endlosschleife bekommen.
        # object.__setattr__(self, name, value) ruft direkt das Standardverhalten von Python 
        # zum Setzen eines Attributs auf, ohne das eigene __setattr__ noch einmal auszulösen. 
        # Dadurch vermeidet man eine Endlosschleife, wenn man selbst __setattr__ überschrieben hat.
        
        # if not os.path.exists(self._log_filename):

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'driving_data/driving_data.csv')      

        object.__setattr__(self, "_start_time", time.time())
        object.__setattr__(self, "_log_filename", filename)

        with open(self._log_filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['Time']+self.csv_col_name_of_fieldnames)

        filename = os.path.join(dirname, 'software/config.json')
        turning_offset = 0
        forward_A = 0
        forward_B = 0
        try:
            with open(filename, "r") as config_file:
                json_data = json.load(config_file)
                turning_offset = json_data["turning_offset"]
                forward_A = json_data["forward_A"]
                forward_B = json_data["forward_B"]
                print(f"Using car params: turning_offset = {turning_offset}, forward_A = {forward_A}, forward_B = {forward_B}")
        except Exception as e:
            print("Error reading config file: ", e)

        self._fw = FrontWheels(turning_offset=turning_offset)       
        self._bw = BackWheels(forward_A=forward_A, forward_B=forward_B)
        self._bw.stop()

        self._steering_angle = 90
        self._speed = 0
        self._direction = 0

        # Jetzt "öffentliche" Attribute setzen
        # (ruft  __setattr__ auf und schreibt damit in die CSV)
        self.steering_angle = 90
        self.speed = 0


    def __setattr__(self, name, value):
        """
        Überschreiben von __setattr__:
        - Loggt alle Zuweisungen an "öffentliche" Attribute (ohne führenden Unterstrich)
          in eine CSV-Datei zusammen mit Zeitstempel.
        - Verhindert Endlosschleifen durch Aufruf von object.__setattr__.
        """

        # Tatsächliches Setzen des Attributs
        object.__setattr__(self, name, value)

        # Prüfen, ob wir das Loggen wollen:
        # Nicht loggen, wenn es sich um ein "privates" Attribut handelt
        # oder speziell get_log / _log_filename / _log etc.
        if not name.startswith("_"):
            # print(f"__setattr__ called with {name}, {value}")
            t = round(time.time() - self._start_time, 2)

            current_values = []
            for prop in self.fieldnames_to_log:
                try:
                    v = getattr(self, str.lower(prop))

                    if isinstance(v, list):
                        for x in v:
                            current_values.append(x)
                    else:
                        current_values.append(v)
                    # print(f"t = {t}, Prop = {prop}, CurrentValues = {current_values}")
                except AttributeError:
                    # Falls _speed etc. noch nicht existiert, None anhängen                    
                    current_values.append(None)
                    # abort logging if not all values are set
                    return

            row = [t] + current_values

            # In CSV-Datei anhängen
            with open(self._log_filename, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(row)



    # def __setattr__(self, name, value):
    #     print(f"--> BaseCar setattr: set {name} to {value}")
    #     object.__setattr__(self, name, value)
        
    ''' getter-method of steering angle'''
    @property
    def steering_angle(self):
        """ Property for steering angle

        Return:
            int: steering angle of the car in degrees in range [45..135]
        """
        return self._steering_angle
    
    ''' setter-method of steering angle'''
    @steering_angle.setter
    def steering_angle(self, angle):
        """ Setter for the property steering angle

        Parameters:
            int: steering angle of the car in degrees in range [45..135]
        """
        if self._steering_angle == angle:
            return
        
        set_angle = self._fw.turn(angle)
        self._steering_angle = set_angle        
        time.sleep(0.1)

    ''' getter-method of speed'''
    @property
    def speed(self):
        """ Property for the speed of the car

        Return:
            int: speed of the car in degrees in range [0..100]
        """
        return self._speed
    
    ''' setter-method of speed'''
    @speed.setter
    def speed(self, speed):
        """ Setter for the speed of the car

        Parameters:
            int: speed of the car in degrees in range [0..100]
        """
        if self._speed == speed:
            return
        
        # Limit parameter values
        if speed < -100:
            self._speed = -100
            print(f'speed was set to {self._speed}')
        elif speed > 100:
            self._speed = 100
            print(f'speed was set to {self._speed}')
        else:
            self._speed = speed

        # calculate direction
        if self._speed < 0:
            if self._direction != -1:
                self._direction = -1
        elif self._speed > 0:
            if self._direction != 1:
                self._direction = 1
        else:
            if self._direction != 0:
                self._direction = 0

        self._bw.speed = abs(self._speed)

    ''' getter-method of direction'''
    @property   
    def direction(self):
        """ Property for the direction of the car

        Return:
            int: direction of the car. Possible values:
                0: no direction because car is not moving
                1: car is moving forward
                -1: car is moving backward
        """
        return self._direction

    def drive(self, speed=None, steering_angle=None):
        """" Start moving the car 
        
        ...with the given parameters. 
        If the values of a paramter is empty the internal values will be used.

        Parameters:
            speed int(): speed of the car in range [45..135]
            steering_angle int(): steering angle of the car in degrees in range [45..135]
        
        """
        if self._speed == speed and self._steering_angle == steering_angle:
            # needed values already set
            # nothing to do
            return
        
        drctn = self._direction
        
        # set steering angle before start driving        
        if not steering_angle is None:
            self.steering_angle = steering_angle

        # set speed and start driving
        if not speed is None:
            self.speed = speed

        if drctn != self._direction:
            if self.direction == 1:
                print(f'Drive Forward with speed {self._speed}')
                self._bw.forward()
            elif self.direction == -1:
                print(f'Drive Backward with speed {self._speed}')
                self._bw.backward()
            else:
                print(f'Stop Driving with speed {self._speed}')
                self._bw.stop()

    def stop(self):
        """" Stop moving the car 
        
        Stops the car as set the steering angle to 90 degrees.
        
        """
        self.drive(0,90)

