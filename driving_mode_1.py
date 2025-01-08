from basecar import *

# initial value from basecar 
bc = BaseCar()
my_speed = 20

try:
    print(f'Start driving - set only speed')
    bc.drive(speed = my_speed)
    time.sleep(3)

    print(f'Stop driving')
    bc.stop()
    time.sleep(1)

    print(f'Start driving - set only speed')
    bc.drive(speed = -my_speed)
    time.sleep(3)

except Exception as e:
  print(f"An exception occurred: {e}") 
  bc.stop()

finally:
  print("Everything ok!") 
  bc.stop()
