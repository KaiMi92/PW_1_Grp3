from basecar import *

# initial value from basecar 
bc = BaseCar()

try:
    print(f"current angle = {bc.steering_angle}")

    # invalid value, expecting 45 (limit to the left)
    bc.steering_angle = 40
    print(f"current angle = {bc.steering_angle}")

    # valid value
    bc.steering_angle = 100
    print(f"current angle = {bc.steering_angle}")

    # invalid value, expecting 135 (limit to the right)
    bc.steering_angle = 140
    print(f"current angle = {bc.steering_angle}")

    # back to value 90 -> straight ahead
    bc.steering_angle = 90
    print(f"current angle = {bc.steering_angle}")

    # -120
    bc.speed = -120
    print(f'direction = {bc.direction}')
    # 0
    bc.speed = 0
    # 50
    bc.speed = 50
    # 0
    bc.speed = 0
    print(f'direction = {bc.direction}')
    # 120
    bc.speed = 120
    print(f'direction = {bc.direction}')
    time.sleep(1)
    #101
    bc.speed = 0
    print(f"speed = {bc.speed}")
    print(f'direction = {bc.direction}')

    print(f'Start driving - no parameters')
    bc.drive()
    time.sleep(1)

    print(f'Start driving - set only steering angle')
    bc.drive(steering_angle = 100)
    time.sleep(1)

    print(f'Start driving - set only speed')
    bc.drive(speed = 40)
    time.sleep(1)

    print(f'Start driving - set speed and steering angle')
    bc.drive(speed = 60, steering_angle = 80)
    time.sleep(1)

    print(f'Start driving - set speed and steering angle')
    bc.drive(speed = -50, steering_angle = 90)
    time.sleep(1)

except:
  print("An exception occurred") 
  bc.stop()

finally:
  print("Everything ok!") 
  bc.stop()
