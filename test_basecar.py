from basecar import *

# initial value 90 -> straight ahead
bc = basecar(90)
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


# -1
bc.speed = -1
# 0
bc.speed = 0
# 50
bc.speed = 50
# 0
bc.speed = 0
# 100
bc.speed = 100
#101
bc.speed = 0
print(f"speed = {bc.speed}")
