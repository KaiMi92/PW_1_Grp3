""" implementation of driving mode 5

implements the requirements of Code2Camp project phase 1

author: Team 3 / Gen 8
"""
from sensorcar import *

# Python Modul Zeit wird als Grundfunktion aufgerufen um später einen Zeitstempel für die gemessen Daten zu erhalten 
import time

# Python Modul Statistik wird als Grundfunktion aufgerufen um statistische Werte wie Median oder Durchschnitt ermitteln zu können 
import statistics

import random

# Setzen der Konstantwerte für Geschwindigkeit und Lenkwinkel Geradeaus, maximal Links und maximal rechts
SPEED = 30
STRAIGHT_FORWARD = 90
MAX_TURN_LEFT = 45
MAX_TURN_RIGHT = 135

# 
# 
def is_end_of_road(ir_values):  
  """
  checks if end of road is reached

  end of roads is detected, when a black line 
  of all sub-sensors or none of the sub-sensors
  is detected

  Parameters:
      ir_values: list
        value list of the ir-sensors
      
  Returns:
      boolean: True if end of road is reached, False elsewhere

  """
  eor = statistics.mean(ir_values) > 0.8
  if eor:
    print(f"End of road detected: {ir_values}, mean = {statistics.mean(ir_values)}")
  return eor

def get_average(l):
  """ Calculate the average from the given list

  Parameters: 
    l: list
        list with number to calculate the avg
      
  Returns:
      float: average of all the numbers from the list

  """
  sum = 0

  for i in l:
    sum = sum + i

  return sum/len(l)

# check if curve is too tight
def is_curve_too_tight(ir_values):
  """
  Checks whether a curve is too tight.

  If this is the case, a full steering lock is not enough and the vehicle must reverse.
  A too tight curve is recognized no black line is detected. So the functions checks
  if the minimun sensor value is bright enough.

  Parameters:
      ir_values: list
        value list of the ir-sensors
      
  Returns:
      boolean: True if curve is too tight, False elsewhere

  """
  ctt = get_average(ir_values) < 0.1
  if ctt:
    print(f"Curve is too tight: {ir_values}, mean = {get_average(ir_values)}")
  return ctt


def get_steering_angle_by_analog_ir_values(ir_values):
  """
  Get the cars speed depending on the values of the IR sensors.

  To calculate the steering angle the functions finds the mean of the indexes
  of the minimum of the analog IR values.
  Depending on the position the steering angle is returned.

  Parameters:
      ir_values: list
        value list of the ir-sensors
      
  Returns:
      steering_angle: int
        steering_angle in degrees

  """
  # we got a list of 5 values
  steering_angle = STRAIGHT_FORWARD

  # lets found all positions of the minimum
  min_val_idxs = [ x for x in range(len(ir_values)) if ir_values[x] == min(ir_values)]
  # calculate the mean of all positions of the minimum
  min_pos = statistics.mean(min_val_idxs)
  print(f"{ir_values} -> min_pos = {min_pos}")
# hier wird ermittelt welcher der Infrarotsensoren den niedrigensten Wert hat bzw. auf den Klebestreifen schaut und entsprechen ein Winkel eingeschlagen um das Fahrzeug in der Mitte des Streifens zu halten
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


def get_steering_angle_by_digital_ir_values(ir_values):
  """
  Get the cars speed depending on the values of the IR sensors.

  To calculate the steering angle the functions finds the mean of the indexes
  of the minimum of the analog IR values.
  Depending on the position the steering angle is returned.

  Parameters:
      ir_values: list
        value list of the ir-sensors
      
  Returns:
      steering_angle: int
        steering_angle in degrees

  """
  # we got a list of 5 values
  steering_angle = STRAIGHT_FORWARD
  new_speed = SPEED

  # lets found all positions of the maximum (->black)
  max_val_idxs = [ x for x in range(len(ir_values)) if ir_values[x] == max(ir_values)]
  # calculate the mean of all positions of the minimum
  max_pos = get_average(max_val_idxs)
  # hier wird ermittelt welcher der Infrarotsensoren den höchste Wert hat bzw. auf den Klebestreifen schaut und entsprechen ein Winkel eingeschlagen um das Fahrzeug in der Mitte des Streifens zu halten

  #  max_pos = 4 --> 45 (MAX_TURN_LEFT)
  #  max_pos = 0 --> 135 (MAX_TURN_RIGHT)

  # calulate the percentage from max_pos between 0.0 and 4.0 
  percentage = max_pos / 4.0
  steering_angle = MAX_TURN_LEFT + int(percentage * (MAX_TURN_RIGHT - MAX_TURN_LEFT))

  if 0.40 <= percentage <= 0.6:
    new_speed = 80
  elif (0.25 <= percentage <= 0.4) or (0.6 <= percentage <= 0.75):
    new_speed = 50
  else:
    new_speed = SPEED  

  # print(f"{ir_values} -> max_pos = {max_pos}, turn to {steering_angle}")
  print(f"{ir_values}, max_pos = {max_pos}, % = {percentage}, angle = {steering_angle}, speed = {new_speed}")
  return steering_angle, new_speed



def get_speed_by_ir_values(ir_values):
  return 0

# Methode main wird definiert und beschrieben
def dm5():
  """
  Implements the driving mode 5 and driving mode 6.

  The cars is driving in loop while not end of road is detected.
  While driving the car is following a black line on the ground also in curves.
  If the curve is too tight the car drives back for a short while and 
  start driving again.

  Parameters:
      None
      
  Returns:
      None

  """  
  sc = SensorCar()

  # check ir sensor
  # while True:
  #   v = sc.analog_values
  #   # print(f"{v} - {get_steering_angle_by_ir_values(v)}")
  #   print(f"{v}")
  #   time.sleep(0.1)

  # start driving (and steering)
  try:  
    sc.drive(speed = SPEED, steering_angle = STRAIGHT_FORWARD)      
  # Schleife wenn alle InfrarotSensoren dunkel sind stopt das Auto der Wert in v wird abgeglichen
    while not BaseCar.finished:
      v = sc.digital_values

      if is_end_of_road(v):
        sc.stop()
        break

      if is_curve_too_tight(v):
        current_steering_angle = sc.steering_angle
        if (current_steering_angle > STRAIGHT_FORWARD):
          sc.drive(speed = -SPEED, steering_angle = MAX_TURN_LEFT)
        if (current_steering_angle < STRAIGHT_FORWARD):
          sc.drive(speed = -SPEED, steering_angle = MAX_TURN_RIGHT)
        else:
          sc.drive(speed = -SPEED, steering_angle = STRAIGHT_FORWARD)
          
        # time.sleep(0.5)  
        time.sleep(random.randint(3, 9)/10)
        
        sc.drive(speed = SPEED, steering_angle = STRAIGHT_FORWARD)      
    # hier wird über die Bedingungen in Zeile 43 bis 53 der Lenkwinkel ermittelt und eingeschlagen alle 0.1 Sekunden
      angle, new_speed = get_steering_angle_by_digital_ir_values(v)
      sc.steering_angle = angle

      time.sleep(0.1)
  except Exception as e:
    print(f"An exception occurred: {e}")
    sc.stop()
  finally:
    print("Everything ok!")
    sc.stop()

if __name__ == "__main__":
  dm5()

