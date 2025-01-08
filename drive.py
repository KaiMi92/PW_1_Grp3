from basecar import *

if __name__ == "__main__":
    auto = Auto()
    setspeed = 50
    turnangle = 120

    auto.drive(turnangle, setspeed)
    time.sleep(2)
    auto.stop()

        
