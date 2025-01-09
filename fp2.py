from basecar import *

if __name__ == "__main__":
    auto = Auto()
    setspeed = 50
    turnangle = 90
    turnangle2 = 135
    turnangle3 = 45

    
    try:
        auto.drive(turnangle, setspeed)
        print(f"Lenkwinkel: {turnangle}, Speed: {setspeed}")

        time.sleep(1)

        auto.stop()

        time.sleep(1)

        auto.drive(turnangle2, setspeed)

        time.sleep(8)

        auto.stop()

        auto.drive(turnangle2, -abs(setspeed))

        auto.stop()

        auto.drive(turnangle3, setspeed)

        time.sleep(8)

        auto.stop()

        auto.drive(turnangle3, -abs(setspeed)) 

        time.sleep(8)


    finally:
        print("Fertig")
        auto.stop()