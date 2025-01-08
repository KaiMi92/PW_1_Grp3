from basecar import *

if __name__ == "__main__":
    auto = Auto()
    auto.speed = 50
    auto.steering_angle = 135
    print(f"Gang: {auto.direction}, Speed: {auto.speed}")