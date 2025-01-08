from basecar import *

# initial value from basecar 
bc = BaseCar()
my_speed = 30
#my_angle

try:
    print(f'Start driving - set only speed')
    #bc.drive(speed = my_speed)
    bc.drive(speed = my_speed, steering_angle = 90)
    time.sleep(1)

    print(f'Stop driving')
    bc.stop()
    time.sleep(1)

    print(f'Start driving - set only speed')
    bc.drive(speed = my_speed, steering_angle = 135)
    time.sleep(8)

except Exception as e:
  print(f"An exception occurred: {e}") 
  bc.stop()

finally:
  print("Everything ok!") 
  bc.stop()
