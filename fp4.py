from basecar import *
from sonic import *
from drive_data import *

if __name__ == "__main__":
    auto = Auto()
    sonic = SonicCar()
    setspeed = 30
    turnangle = 90
    trys = 0

    try:
        auto.drive(turnangle, setspeed)

        while trys < 5:
            while True:
                s = sonic.get_sonic()
                if s < 20 and s > 0:
                    auto.stop()
                    print("Hindernis")
                    break
            save_data()
            auto.drive(135, -setspeed)
            time.sleep(2)
            auto.drive(turnangle, setspeed)
            trys +=1             

        auto.stop()
        print("5x versucht, Hindernis immer noch da")

    except:
        print("error")