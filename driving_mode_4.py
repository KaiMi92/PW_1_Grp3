from soniccar import *
sc = SonicCar()
 
my_speed = 40
my_angle = 90
STRAIGHT_FORWARD = my_angle
MIN_DISTANCE = 20
max_turn_left = 45
max_turn_right = 135
counter = 0
 
 
try:  
  sc.drive(speed = my_speed, steering_angle = STRAIGHT_FORWARD)      
 
  while counter < 5: 
    while True:
      d = sc.get_distance()
      if d < MIN_DISTANCE and d > 0:
        sc.stop()
        time.sleep(0.5)
        break
    sc.drive(speed = -my_speed, steering_angle = max_turn_left)
    time.sleep(3)
    counter += 1
  sc.stop()

except Exception as e:
  print(f"An exception occurred: {e}")
  sc.stop()
 
finally:
  print("Everything ok!")
  sc.stop()