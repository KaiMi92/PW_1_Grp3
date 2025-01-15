from basecar import *

'''
initial value from basecar
''' 
bc = BaseCar()
my_speed = 20

'''
try block let us try different speeds 
  time.sleep: The command is used to set the time to be traveled
  speed:  sets the speed between -100 and 100, with the positive
          the positive values for driving forwards and the negative values
          for driving backwards
  bc.drive: imports the drive function from the basecar class
'''

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
