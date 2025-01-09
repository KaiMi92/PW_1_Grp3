from basecar import *

if __name__ == "__main__":
    auto = Auto()
    setspeed = 30
    setspeed2 = -30
    turnangle = 90
    turnangle2 = 120
    turnangle3 = 60

    
    try:
        auto.drive(turnangle, setspeed)
        print(f"Lenkwinkel: {turnangle}, Speed: {setspeed}")

        time.sleep(1)

        auto.drive(turnangle2, setspeed)

        time.sleep(8)

        auto.drive(turnangle2, setspeed2)

        time.sleep(8)

        auto.drive(turnangle3, setspeed)

        time.sleep(8)

        auto.drive(turnangle3, setspeed2) 

        time.sleep(8)


    finally:
        print("Fertig")
        auto.stop()