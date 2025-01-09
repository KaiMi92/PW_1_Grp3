from basecar import *
from sonic import *
import sys

if __name__ == "__main__":
    bc = Auto()
    so = SonicCar()
    drivedata = {}

    a = so.get_sonic()
    b = bc.direction
    c = bc.speed
    d = bc.steering_angle
    drivedata = {"Sonic":[a], "Direction":[b], "Speed":[c], "Steering":[d] }

    print(drivedata)