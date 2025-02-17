from basecar import *

'''
try block let us try different speeds 
  bc.drive: imports the driving and steering functions from the basecar class
  steering_angle:   45 degrees -> maximum steering angle to the left
                    90 degrees -> angle for driving straight ahead
                    135 degrees -> maximum steering angle to the right
                    
'''
def dm2():
  
  '''
  initial value from basecar
  ''' 

  bc = BaseCar()
  my_speed = 60
  my_angle = 135


  try:
    
    if not BaseCar.finished:
      print(f'Start driving - set only speed')
      bc.drive(speed = my_speed, steering_angle = 90)
      time.sleep(1)
      #stop befor next step
      print(f'Stop driving')
      bc.stop()
      time.sleep(1)

    if not BaseCar.finished:
      #cycle driving
      print(f'Start driving - set only speed')
      bc.drive(speed = my_speed, steering_angle = my_angle)
      time.sleep(8)

    if not BaseCar.finished:
      #stop befor next step
      print(f'Stop driving')
      bc.stop()
      time.sleep(1)

    if not BaseCar.finished:
      #cycle driving
      print(f'Start driving - set only speed')
      bc.drive(speed = -my_speed, steering_angle = my_angle)
      time.sleep(8)

    if not BaseCar.finished:
      #stop befor next step
      print(f'Stop driving')
      bc.stop()
      time.sleep(1)

    if not BaseCar.finished:
      print(f'Start driving - set only speed')
      #bc.drive(speed = my_speed)
      bc.drive(speed = -my_speed, steering_angle = 90)
      time.sleep(1)

  except Exception as e:
    print(f"An exception occurred: {e}") 
    bc.stop()

  finally:
    print("Everything ok!") 
    bc.stop()
if __name__ == "__main__":
   dm2()
