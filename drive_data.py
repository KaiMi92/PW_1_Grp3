from basecar import *
from sonic import *
import sys
import csv

def save_data():
    bc = Auto()
    so = SonicCar()
    drivedata = {}

    a = so.get_sonic()
    b = bc.direction
    c = bc.speed
    d = bc.steering_angle
    drivedata = [{"Sonic": a, "Direction": b, "Speed": c, "Steering": d}]

    print(drivedata)

    with open('fahrdaten.csv', 'a+', newline='') as f:
        field_names = ['Sonic', 'Direction', 'Speed', 'Steering']
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writerows(drivedata)

#if __name__ == "__main__":
#    save_data()