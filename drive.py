from basecar import *

if __name__ == "__main__":
    auto = Auto()
    setspeed = -50
    turnangle = 90

    
    try:
        auto.drive(turnangle, setspeed)
        print(f"Lenkwinkel: {turnangle}, Speed: {setspeed}")

        time.sleep(3)

    finally:
        print("Fertig")
        auto.stop()
        
