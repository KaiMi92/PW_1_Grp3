from soniccar import * 

# Diese Klasse verwendet den IR-Sensor
class SensorCar(SonicCar):
    def __init__(self) -> None:
        self.ir = Infrared()
        super().__init__()

    @property
    def analog_values(self):
        """
        Getter- um die gemessenen IR-Werte in Form einer Liste auszulesen
        Return: Liste von gemessen IR-Werten der Sensoren
        """
        return self.ir.read_analog()
    
    @property
    def digital_values(self):
        """
        Getter- um die gemessenen IR-Werte in Form einer Liste auszulesen
        Return: Liste von gemessen IR-Werten der Sensoren
        """
        return self.ir.read_digital()