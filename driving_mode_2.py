from basecar import *
def dm2():
# initial value from basecar 
  bc = BaseCar()
  my_speed = 60
  my_angle = 135

  try:
      #needed for video
      time.sleep(3)
      
      print(f'Start driving - set only speed')
      #bc.drive(speed = my_speed)
      bc.drive(speed = my_speed, steering_angle = 90)
      time.sleep(1)
      #stop befor next step
      print(f'Stop driving')
      bc.stop()
      time.sleep(1)

      #cycle driving
      print(f'Start driving - set only speed')
      bc.drive(speed = my_speed, steering_angle = my_angle)
      time.sleep(8)

      #stop befor next step
      print(f'Stop driving')
      bc.stop()
      time.sleep(1)

      #cycle driving
      print(f'Start driving - set only speed')
      bc.drive(speed = -my_speed, steering_angle = my_angle)
      time.sleep(8)

      #stop befor next step
      print(f'Stop driving')
      bc.stop()
      time.sleep(1)

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
