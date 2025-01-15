import pandas as pd 
import numpy as np

''' 
Import the csv file and separate the columns “Speed” and “Time” 
columns for further calculations
'''

path = "driving_data/driving_data.csv"
skip_var = 0
try:
    drive_data = pd.read_csv(path)
    skip_var = 0
except pd.errors.EmptyDataError:
    print("CSV File empty")
    skip_var = 1
    

'''
.max -> searches for the highest value of the vector
.min -> searches for the minimum value of the vector
.mean -> calculates the average value
'''

#max speed
max_speed = data_speed.max()
print(f'Max speed:',max_speed)
#min speed
min_speed = data_speed.min()
print(f'Min speed:',min_speed)
#average speed
average_speed = data_speed.mean()
print(f'Average speed:', average_speed)

'''
drive_data
    variable to obtain the time difference between the line entries,
    the difference between the rows is calculated with the .diff command

distances
    as the time difference must be calculated with the previous speed.
    the first entry of the vector must be deleted. ->[:-1]
    To calculate the distance traveled, the sum must be calculated with sum()
'''

#driven distance  
drive_data['time_diff'] = drive_data["Time"].diff()
distances = drive_data['time_diff'][1:].values * drive_data['Speed'][:-1].values
driven_distance = sum(distances)
print(f'Driven distance:' ,driven_distance)
