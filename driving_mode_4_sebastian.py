from soniccar import *
import time

sc = SonicCar()

STRAIGHT_FORWARD = 90
MIN_DISTANCE = 20
MAX_TURN_LEFT = 45
MAX_TURN_RIGHT = 135

# get the cars speed depending on the distance to an obstacle
def get_speed_by_distance(dist):
  if dist > 100:
    speed = 50
  elif dist < 0:
    speed = 0
  else:
    speed = max (18, dist // 2)
  return speed


# try to get distance for max 5 seconds
def get_distance_with_timeout():
  t_end = time.time() + 5
  d = sc.get_distance()
  while d < 0 and time.time() < t_end:
    d = sc.get_distance()
    time.sleep(0.5)
  return d


# drive and stop before crash with an obstacle
def drive_to_the_obstacle():
  last_time_with_pos_dist = time.time()
  while True:
    d = get_distance_with_timeout()
    if d > 0 and d < MIN_DISTANCE:
      sc.stop()
      last_time_with_pos_dist = time.time()
      time.sleep(0.1)
      break

    # if the car is get stuck -> break
    if last_time_with_pos_dist + 5 < time.time():
      break

    sc.drive(speed = get_speed_by_distance(d), steering_angle = STRAIGHT_FORWARD)
  time.sleep(1)


# drive back for # seconds with steering MAX_TURN_LEFT
def drive_back_and_turn():
  sc.drive(speed = -30, steering_angle = MAX_TURN_LEFT)
  time.sleep(3)
  sc.stop()
  time.sleep(1)
  sc.steering_angle = STRAIGHT_FORWARD


def main():
  # get distance before start
  # d = get_first_distance()
  # my_speed = get_speed_by_distance(d)

  # start driving
  try:  
    # sc.drive(speed = my_speed, steering_angle = STRAIGHT_FORWARD)      
  
    while True:
      drive_to_the_obstacle()
      drive_back_and_turn()

  except Exception as e:
    print(f"An exception occurred: {e}")
    sc.stop()
  finally:
    print("Everything ok!")
    sc.stop()

if __name__ == "__main__":
  main()

