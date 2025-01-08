from basecar import *

if __name__ == "__main__":
    auto = Auto()
    auto.speed = 0
    auto.steering_angle = 90
    print(f"Gang: {auto.direction}, Speed: {auto.speed}")