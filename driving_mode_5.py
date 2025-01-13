from sensorcar import *
import time
import statistics

sc = SensorCar()

SPEED = 30
STRAIGHT_FORWARD = 90
MAX_TURN_LEFT = 45
MAX_TURN_RIGHT = 135

# checks if end of road is reached
# end of roads is detected, when a black line 
# of all sub-sensors or none of the sub-sensors
# is detected
def is_end_of_road(ir_values):
  eor = statistics.mean(ir_values) < 80
  if eor:
    print(f"End of road detected: {ir_values}")
  return eor

# check if curve is too tight
def is_curve_too_tight(ir_values):
  ctt = min(ir_values) > 100
  if ctt:
    print(f"Curve is too tight: {ir_values}")
  return ctt


# get the cars speed depending on the distance to an obstacle
def get_steering_angle_by_ir_values(ir_values):
  # we got a list of 5 values
  steering_angle = STRAIGHT_FORWARD

  # lets found all positions of the minimum
  min_val_idxs = [ x for x in range(len(ir_values)) if ir_values[x] == min(ir_values)]
  # calculate the mean of all positions of the minimum
  min_pos = statistics.mean(min_val_idxs)
  print(f"{ir_values} -> min_pos = {min_pos}")

  if min_pos < 1:
    steering_angle = MAX_TURN_LEFT
  elif min_pos <= 2:
    steering_angle = STRAIGHT_FORWARD - 23
  elif min_pos <= 3:
    steering_angle = STRAIGHT_FORWARD
  elif min_pos <= 4:
    steering_angle= STRAIGHT_FORWARD + 23
  else:
    steering_angle = MAX_TURN_RIGHT

  return steering_angle


def main():
  # check ir sensor
  # while True:
  #   v = sc.analog_values
  #   # print(f"{v} - {get_steering_angle_by_ir_values(v)}")
  #   print(f"{v}")
  #   time.sleep(0.1)

  # start driving (and steering)
  try:  
    sc.drive(speed = SPEED, steering_angle = STRAIGHT_FORWARD)      
  
    while True:
      v = sc.analog_values

      if is_end_of_road(v):
        sc.stop()
        break

      if is_curve_too_tight(v):
        sc.drive(speed = -SPEED, steering_angle = STRAIGHT_FORWARD)
        time.sleep(1.0)      
        sc.drive(speed = SPEED, steering_angle = STRAIGHT_FORWARD)      
    
      angle = get_steering_angle_by_ir_values(v)
      sc.steering_angle = angle

      time.sleep(0.1)
  except Exception as e:
    print(f"An exception occurred: {e}")
    sc.stop()
  finally:
    print("Everything ok!")
    sc.stop()

if __name__ == "__main__":
  main()

