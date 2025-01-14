from soniccar import *

fieldnames = ['Time','Distance','Direction','Speed','Steering','IR-v1','IR-v2','IR-v3','IR-v4','IR-v5']
setter_of_fieldnames = ['-','_distance','_direction','_speed','_steering_angle', '_ir_values']

# Diese Klasse verwendet den IR-Sensor
class SensorCar(SonicCar):
    def __init__(self) -> None:
        self.ir = Infrared()
        self._start_time = time.time()
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'driving_data/driving_data.csv')        
        self._csv_file = open(filename, 'w', newline='')
        self._writer = csv.DictWriter( self._csv_file, fieldnames=fieldnames)
        self._writer.writeheader()  

        self._ir_values = (300,300,300,300,300)
        super().__init__()

    def lists_have_same_values(self, l1, l2):
        if len(l1) != len(l2):
            return False
        
        for i in range(len(l1)):
            if l1[i] != l2[i]:
                return False
            
        return True


    @property
    def analog_values(self):
        """
        Getter- um die gemessenen IR-Werte in Form einer Liste auszulesen
        Return: Liste von gemessen IR-Werten der Sensoren
        """
        values = self.ir.read_analog()

        if not self.lists_have_same_values(self._ir_values, values):
            self._ir_values = values

        return self.ir.read_analog()
    
    @property
    def digital_values(self):
        """
        Getter- um die gemessenen IR-Werte in Form einer Liste auszulesen
        Return: Liste von gemessen IR-Werten der Sensoren
        """
        return self.ir.read_digital()

    
    def __setattr__(self, name, value):
        # print(f"--> SonicCar setattr: set {name} to {value}")
        try:
            object.__setattr__(self, name, value)

            if name in setter_of_fieldnames:
                t = round(time.time() - self._start_time, 2)
                data = [{'Time': t, 'Distance': self._distance, 'Direction': self._direction, 'Speed': self._speed, 'Steering': self._steering_angle, 'IR-v1': self._ir_values[0], 'IR-v2': self._ir_values[1], 'IR-v3': self._ir_values[2], 'IR-v4': self._ir_values[3], 'IR-v5': self._ir_values[4]}]
                self._writer.writerows(data)
                print(f"Write CSV: {data}")
        except Exception as e:
            print(f"{__name__}: An exception occurred: {e}")