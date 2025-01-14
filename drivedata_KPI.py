import pandas as pd 
import numpy as np


drive_data = pd.read_csv('drivedata.csv')
#print(drive_data)
data_speed = drive_data["Speed"]
data_time = drive_data['Time']
sum_time = data_time.sum()

#max speed
max_speed = data_speed.max()
#print(f'Max speed:',max_speed)
#min speed
min_speed = data_speed.min()
#print(f'Min speed:',min_speed)
#average speed
average_speed = data_speed.mean()
#print(f'Average speed:', average_speed)
#driven distance  
drive_data['time_diff'] = drive_data["Time"].diff()
#drive_data = drive_data.dropna().reset_index()
distances = drive_data['time_diff'][1:].values * drive_data['Speed'][:-1].values
driven_distance = sum(distances)
#print(drive_data)
#print('Test', time_diff)
print(f'Driven distance' ,driven_distance)
#distance_traveled_sum = driven_distance.sum()
#print(distance_traveled_sum)
print(drive_data["Speed"])
print(drive_data["Speed"].values)
