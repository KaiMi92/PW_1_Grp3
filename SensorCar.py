from soniccar import * 

# Diese Klasse verwendet den IR-Sensor
class Infred(SonicCar):
    def __init__(self) -> None:
        super().__init__()
        self.ir = Infrared()

    @property
    def ir_werte(self):
        """
        Getter- um die gemessenen IR-Werte in Form einer Liste auszulesen
        Return: Liste von gemessen IR-Werten der Sensoren
        """
        return self.ir.read_analog()