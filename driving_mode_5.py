from sensorcar import *
import time
import statistics

sc = SensorCar()

STRAIGHT_FORWARD = 90
MIN_DISTANCE = 20
MAX_TURN_LEFT = 45
MAX_TURN_RIGHT = 135

# get the cars speed depending on the distance to an obstacle
def is_end_of_road(ir_values):
  return min(ir_values) > 2

# get the cars speed depending on the distance to an obstacle
def get_steering_angle_by_ir_values(ir_values):
  # we got a list of 5 values
  steering_angle = STRAIGHT_FORWARD

  # lets found the pos of the minimum
  min_val_idxs = [ x for x in range(len(ir_values)) if ir_values[x] == min(ir_values)]
  min_pos = statistics.mean(min_val_idxs)

  if min_pos < 1:
    steering_angle = MAX_TURN_LEFT
  elif min_pos <= 2:
    steering_angle = STRAIGHT_FORWARD - 15
  elif min_pos <= 3:
    steering_angle = STRAIGHT_FORWARD
  elif min_pos <= 4:
    steering_angle= STRAIGHT_FORWARD + 15
  else:
    steering_angle = MAX_TURN_RIGHT

  return steering_angle

# try to get distance for max 5 seconds
def get_ir_values_with_timeout():
  t_end = time.time() + 5
  d = sc.analog_values
  # while d < 0 and time.time() < t_end:
  #   d = sc.get_distance()
  #   time.sleep(0.5)
  return d


# drive and stop before crash with an obstacle
def drive_to_the_obstacle():
  # sc.drive(speed = 30, steering_angle = STRAIGHT_FORWARD)
  while True:
    v = sc.analog_values
    if is_end_of_road(v):
      sc.stop()
      break
    
    angle = get_steering_angle_by_ir_values(v)
    sc.steering_angle = angle

    time.sleep(0.5)
  time.sleep(1)


def main():
  # check ultrasonic sensor
  # while True:
  #   print(sc.get_distance())
  #   time.sleep(0.1)

  # check ir sensor
  # while True:
  #   v = sc.analog_values
  #   print(f"{v} - {get_steering_angle_by_ir_values(v)}")
  #   time.sleep(0.1)

  # get distance before start
  # d = get_first_distance()
  # my_speed = get_speed_by_distance(d)

  # start driving
  try:  
    # sc.drive(speed = my_speed, steering_angle = STRAIGHT_FORWARD)      
  
    while True:
      v = sc.analog_values
      if is_end_of_road(v):
        sc.stop()
        break
    
      angle = get_steering_angle_by_ir_values(v)
      sc.steering_angle = angle

      time.sleep(0.5)
  except Exception as e:
    print(f"An exception occurred: {e}")
    sc.stop()
  finally:
    print("Everything ok!")
    sc.stop()

if __name__ == "__main__":
  main()

