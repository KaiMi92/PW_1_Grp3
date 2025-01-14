# aus der Klasse Sensorcar werden Methoden übernommen
from sensorcar import *
# Python Modul Zeit wird als Grundfunktion aufgerufen um später einen Zeitstempel für die gemessen Daten zu erhalten 
import time
# Python Modul Statistik wird als Grundfunktion aufgerufen um statistische Werte wie Median oder Durchschnitt ermitteln zu können 
import statistics
def dm5():
  sc = SensorCar()
  # Setzen der Konstantwerte für Geschwindigkeit und Lenkwinkel Geradeaus, maximal Links und maximal rechts
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

  # Methode main wird definiert und beschrieben
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
    # Schleife wenn alle InfrarotSensoren dunkel sind stopt das Auto der Wert in v wird abgeglichen
      while True:
        v = sc.analog_values

        if is_end_of_road(v):
          sc.stop()
          break
        # wenn der Wert über 100 geht in v wird eine Sekunde zurückgefahren und dann wieder weiter. 
        if is_curve_too_tight(v):
          sc.drive(speed = -SPEED, steering_angle = STRAIGHT_FORWARD)
          time.sleep(1.0)      
          sc.drive(speed = SPEED, steering_angle = STRAIGHT_FORWARD)      
      # hier wird über die Bedingungen in Zeile 43 bis 53 der Lenkwinkel ermittelt und eingeschlagen alle 0.1 Sekunden
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
if __name__ == "__main__":
  dm5()
