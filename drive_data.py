from basecar import *
from sonic import *
import sys

if __name__ == "__main__":
    bc = Auto()
    so = SonicCar()
    drivedata = {}

    fill = {bc.steering_angle, bc.speed, so.get_sonic}
    drivedata.update(fill)

    print(drivedata)