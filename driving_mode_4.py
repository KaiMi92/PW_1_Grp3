""" soniccar driving mode 4
Implements an autonomous driving mode with ultrasonic sensors for obstacle detection and avoidance.

author: Tema 3 / Gen 8
"""

from soniccar import *
import time

STRAIGHT_FORWARD = 90
MIN_DISTANCE = 20
MAX_TURN_LEFT = 45
MAX_TURN_RIGHT = 135

# get the cars speed depending on the distance to an obstacle
def get_speed_by_distance(dist):
  """
  Determines the speed based on the distance to an obstacle
  Parameter
  ---------
  dist : int
        Distance to the nearest obstacle (in cm)
  Return
  ------
  int
  Speed of the Car (in percentage). Range from 0 to 100
    If the distance is greater than 100, the speed is set to 100%
    If the distance is below 0, the speed is set to 0
    Otherwise, the speed is calculated as half of the Distance, with max. speed 30%.
  """
  # return 50
  if dist > 100:
    speed = 100
  elif dist < 0:
    speed = 0
  else:
    speed = max (30, dist // 2)
  return speed


# try to get distance for max 5 seconds
def get_distance_with_timeout(sc):
  """
  Measuring the distance to the obstacle using the ultrasonic sensor.

  tries to retrieve a valid distance within a timeout of 5 seconds
  If no obstacle is in range, a default value of 123cm is returned

  Returns
  ------
  int
      Distance to the obstacle (in cm)
      Returns -2 if no valid distance is available
  """
  t_end = time.time() + 5
  d = sc.get_distance()

  # no obstancles in range
  if d == -2:
    d = 123

  while d < 0 and time.time() < t_end:
    d = sc.get_distance()
    time.sleep(0.5)
  return d


# drive and stop before crash with an obstacle
def drive_to_the_obstacle(sc):

  """
  The Car drives forward until an obstacle is detected within the minimum distance
  
  Uses the Data from the ultrasonic sensor to adjust the speed dynamically based on the distance.
  Stops the car when the distance falls below or if no valid distance is available
  """
  # sc.drive(speed = get_speed_by_distance(get_distance_with_timeout()), steering_angle = STRAIGHT_FORWARD)
  while True:
    d = get_distance_with_timeout(sc)
    if d > 0 and d < MIN_DISTANCE:
      sc.stop()
      time.sleep(0.1)
      break

    # if the car is get stuck -> break
    if d < 0:
      print("get stuck , turn over")
      break

    time.sleep(0.5)
    sc.drive(speed = get_speed_by_distance(d), steering_angle = STRAIGHT_FORWARD)
  time.sleep(1)


# drive back for # seconds with steering MAX_TURN_LEFT
def drive_back_and_turn(sc):

  """
  Executes a reversing maneuver followed by a turn.

  The car reverses at a fixed speed and steering angle for 3 seconds,
  then stops and resets the steering angle to straigt forward
  """
  sc.drive(speed = -30, steering_angle = MAX_TURN_LEFT)
  time.sleep(3)
  sc.stop()
  time.sleep(1)
  sc.steering_angle = STRAIGHT_FORWARD


def dm4():
    """   
    Driving Mode 4: Autonomous obstacle avoidance.
    
    The car alternates between driving forward and stopping at obstacles, 
    followed by a reversing and turning maneuver to avoid obstacles.
    This driving loop continues until manually interrupted or an exception occurs.
    """

    sc = SonicCar()

  # check ultrasonic sensor
  # while True:
  #   print(sc.get_distance())
  #   time.sleep(0.1)

  # get distance before start
  # d = get_first_distance()
  # my_speed = get_speed_by_distance(d)

    # start driving
    try:  
      # sc.drive(speed = my_speed, steering_angle = STRAIGHT_FORWARD)      
    
      while not BaseCar.finished:
        drive_to_the_obstacle(sc)
        drive_back_and_turn(sc)
    except Exception as e:
      print(f"An exception occurred: {e}")
      sc.stop()
    finally:
      print("Everything ok!")
      sc.stop()

if __name__ == "__main__":
  dm4()

