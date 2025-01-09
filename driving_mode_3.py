from soniccar import *
sc = SonicCar()
my_speed = 40
my_angle = 90
STRAIGHT_FORWARD = my_angle
MIN_DISTANCE = 20



try:  
  sc.drive(speed = my_speed, steering_angle = STRAIGHT_FORWARD)      
  
  
  while True:
    d = sc.get_distance()
    if d < MIN_DISTANCE and d > 0:
      sc.stop()
      break
    time.sleep(0.5)

except Exception as e:
  print(f"An exception occurred: {e}") 
  sc.stop()

finally:
  print("Everything ok!") 
  sc.stop()

  