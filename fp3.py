from basecar import *
from sonic import *

if __name__ == "__main__":
    auto = Auto()
    sonic = SonicCar()
    setspeed = 30
    turnangle = 90

    try:
        auto.drive(turnangle, setspeed)

        while True:
            s = sonic.


    except:
        print("error")