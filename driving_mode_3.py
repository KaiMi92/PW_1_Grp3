from soniccar import *
sc = SonicCar()

try:        
    d = sc.get_distance()
    print(f'd = {d}')

except Exception as e:
  print(f"An exception occurred: {e}") 
  sc.stop()

finally:
  print("Everything ok!") 
  sc.stop()

  