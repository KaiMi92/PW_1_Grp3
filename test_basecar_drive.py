from basecar import *

# initial value from basecar 
bc = BaseCar()

try:
    # print(f'Start driving - no parameters')
    # bc.drive()
    # time.sleep(1)

    # print(f'Start driving - set only steering angle')
    # bc.drive(steering_angle = 100)
    # time.sleep(1)

    print(f'Start driving - set only speed')
    bc.drive(speed = 40)
    time.sleep(1)

    print(f'Stop driving')
    bc.stop()
    time.sleep(1)

    print(f'Start driving - set only speed')
    bc.drive(speed = -40)
    time.sleep(1)

    # print(f'Start driving - set speed and steering angle')
    # bc.drive(speed = 60, steering_angle = 80)
    # time.sleep(1)

    # print(f'Start driving - set speed and steering angle')
    # bc.drive(speed = -50, steering_angle = 90)
    # time.sleep(2)

except Exception as e:
  print(f"An exception occurred: {e}") 
  bc.stop()

finally:
  print("Everything ok!") 
  bc.stop()
