from soniccar import *

"""
This is the implementation of the requirement for driving mode3.
At the beginning, the information and skills of the Soniccar and basecar classes are read in. 

The car drives at a defined steering angle and speed until an obstacle falls below a set distance. then the vehicle should remain stationary

Author: Team 3 / Gen 8
"""

def dm3():
  sc = SonicCar()
  my_speed = 40
  my_angle = 90
  STRAIGHT_FORWARD = my_angle
  MIN_DISTANCE = 20
  
  """ 
  In this method, the variables for steering angle, speed, 
  minimum distance, and straight ahead are set with my_angle 
  """

  try:  
    sc.drive(speed = my_speed, steering_angle = STRAIGHT_FORWARD)      
    
    
    while True:
      d = sc.get_distance()
      if d < MIN_DISTANCE and d > 0:
        sc.stop()
        break
      time.sleep(0.5)

  except Exception as e:
    print(f"An exception occurred: {e}") 
    sc.stop()

  finally:
    print("Everything ok!") 
    sc.stop()
    """ 
    they are nested loops. the vehicle extends until an obstacle indicates a minimum distance. 
    However, so that error messages from the distance sensors do not lead to a stop of the car, 
    it has been determined here that a stop of the vehicle is only triggered 
    if the measured distance is less than the target of the variable MIN_DINSTANCE but greater than 0, 
    since error messages with negative values such as -2 or -4 are output
    """
if __name__ == ("__main__"):
  dm3()
  """
  Don't understand why the main method comes
  """
  