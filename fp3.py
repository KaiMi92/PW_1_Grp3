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
            s = sonic.get_sonic()
            if s < 20 and s > 0:
                auto.stop()
                print("Hindernis")
                break

    except:
        print("error")