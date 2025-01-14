from turtle import Turtle, Screen
from random import random
import pandas as pd
 
path = "driving_data.csv"
drive_data = pd.read_csv(path)
data_speed = drive_data["Speed"]
data_time = drive_data['Time']
data_steering = drive_data['Steering']
sum_time = data_time.sum()
 
screen = Screen()
print(f"Screen {screen.window_width()} x {screen.window_height()}")    
trtle = Turtle()
trtle.speed('fast')
# screen.tracer(0)
trtle.penup()
#trtle.pensize(5)
trtle.goto(0, -(screen.window_height()/2))
trtle.pendown()
 
last_t = data_time[0]
last_v = data_speed[0]
last_steering = data_steering[0]
 
for i in range(1, len(drive_data)):
    # v = s/t --> s = v * t
    t = data_time[i] - last_t
    v = last_v
    s = v * t
    print(f"Line {i}: v = {v}, s = {s}, t = {t}, steering = {last_steering}")
    steps = int(s*2)
    angle = int(last_steering)
 
    trtle.setheading(angle)
    if s > 0:
        trtle.color("green")
        trtle.fd(steps)
    else:
        trtle.color("red")
        trtle.bk(-steps)
 
    last_t = data_time[i]
    last_v = data_speed[i]
    last_steering = data_steering[i]
 
# t = Turtle()
# for i in range(100):
#     steps = int(random() * 100)
#     angle = int(random() * 360)
#     t.right(angle)
#     t.fd(steps)
# screen.update()
trtle.screen.mainloop()