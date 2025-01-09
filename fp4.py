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
            while True:
                s = sonic.get_sonic()
                if s < 20 and s > 0:
                    auto.stop()
                    print("Hindernis")
                    break
            
            auto.drive(135, -setspeed)
            time.sleep(2)
            auto.drive(turnangle, setspeed)             

    except:
        print("error")