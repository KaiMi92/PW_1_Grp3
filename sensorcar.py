"""SensorCar implementation

SensorCar represents a car with infrared sensors.
It inherits from the class SonicCar and implements
the requirements of Code2Camp project phase 1

Attributes:
    fieldnames: name of all fields which values are logged in the driving log file
    setter_of_fieldnames: name of all setters which values are logged in the driving log file

author: Team 3 / Gen 8
"""
from soniccar import *
"""Implementation in the Sensorcar file

The aim of this class is to complement the Sensorcar class with the functions of infrared sensors. 
Sensorcar should be available as a class later for other driving modes from projectphase 1 
and make the other classes usable, e.g. Basecar and Sensorcar.

author: Team 3 / Gen 8
"""

fieldnames = ['Time','Distance','Direction','Speed','Steering','IR-v1','IR-v2','IR-v3','IR-v4','IR-v5']
setter_of_fieldnames = ['-','_distance','_direction','_speed','_steering_angle', '_ir_values']

class SensorCar(SonicCar):
    """SensorCar implementation

    SensorCar represents a car with infrared sensors.
    It inherits from the class SonicCar and implements
    the requirements of Code2Camp project phase 1

    Attributes
    ----------
        fieldnames: list
            name of all fields which values are logged in the driving log file
        setter_of_fieldnames: list+
            name of all setters which values are logged in the driving log file
        csv_file: file
            the driving log file
        ir_values: list
            values reas from the infrared-sensor
            it consists of 5 values representing the 5 sensors arranged next to each other

    author: Team 3 / Gen 8
    """    

    BaseCar.fieldnames_to_log = BaseCar.fieldnames_to_log + ["analog_values"]
    BaseCar.csv_col_name_of_fieldnames = BaseCar.csv_col_name_of_fieldnames + ['IR-v1','IR-v2','IR-v3','IR-v4','IR-v5']

    def __init__(self) -> None:
        super().__init__()
        self.ir = Infrared()
        self._start_time = time.time()
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'driving_data/driving_data.csv')        
        self._csv_file = open(filename, 'w', newline='')
        self._writer = csv.DictWriter( self._csv_file, fieldnames=fieldnames)
        self._writer.writeheader()  

        self._ir_values = (300,300,300,300,300)
        """ it is determined what the reference values of the IR sensors are with 300 each. 
        A relative path is selected to call up the csv file in which the start time is 
        to be written as the first value with the corresponding values from the sensors, 
        steering angle and speed. 
        with super().__init__() you want to get the distance sensors from the other class Soniccar
        or indirectly the information from basiscar .
        """

    def lists_have_same_values(self, l1, l2):
        """
        Checks if two lists have the same values in the same order

        Parameters:
            l1: one list
            l2: another list
            
        Returns:
            boolean: True if the two given lists have the same values in the 
                same order, else False

        """
        if len(l1) != len(l2):
            return False
        
        for i in range(len(l1)):
            if l1[i] != l2[i]:
                return False
            
        return True
        """Not understood, a comparison is carried out but why?
        """


    @property
    def analog_values(self):
        """
        Getter to read out the measured IR values in the form of a list
        Return: List of measured IR values of the sensors
        """
        values = self.ir.read_analog()

        if not self.lists_have_same_values(self._ir_values, values):
            self._ir_values = values

        return self.ir.read_analog()
    
    @property
    def digital_values(self):
        """
        Getter to read out the measured IR values in the form of a list
        Return: List of measured IR values of the sensors
        """
        return self.ir.read_digital()

    
    # def __setattr__(self, name, value):
    #     """
    #     __setattr__ is one magic function which is called every time a setter is called

    #     With this implementation the standard function is overwritten to write every call
    #     of a setter function in the driving log file. Therefore this function checks if the 
    #     name of the variable is a part of setter_of_fieldnames

    #     Parameters:
    #         name: name of the variable to set
    #         value: value which should be set
    #     """
    #     try:
    #         object.__setattr__(self, name, value)

    #         if name in setter_of_fieldnames:
    #             t = round(time.time() - self._start_time, 2)
    #             data = [{'Time': t, 'Distance': self._distance, 'Direction': self._direction, 'Speed': self._speed, 'Steering': self._steering_angle, 'IR-v1': self._ir_values[0], 'IR-v2': self._ir_values[1], 'IR-v3': self._ir_values[2], 'IR-v4': self._ir_values[3], 'IR-v5': self._ir_values[4]}]
    #             self._writer.writerows(data)
    #             print(f"Write CSV: {data}")
    #     except Exception as e:
    #         print(f"{__name__}: An exception occurred: {e}")
    #         """here the information per row, i.e. measurement time, 
    #         is written to the previously defined columns in the defined CSV file. Time, Distance, 
    #         Direction, Speed, Steering and the 5 IR-values
    #         """