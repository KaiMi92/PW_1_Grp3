from basecar import *

if __name__ == "__main__":
    auto = Auto()
    setspeed = 50
    turnangle = 120
    setgang= 1

    auto.drive(turnangle, setspeed, setgang)
    print(f"Lenkwinkel: {turnangle}, Speed: {setspeed}, Gang: {setgang}")

        
