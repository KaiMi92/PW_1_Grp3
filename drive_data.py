from basecar import *
from sonic import *
import sys

if __name__ == "__main__":
    bc = Auto()
    so = SonicCar()
    drivedata = {}

    x = so.get_sonic()
    drivedata = {bc.steering_angle, bc.speed, x}

    print(drivedata)