import pandas as pd 
path = "driving_data/driving_data.csv"
drive_data = pd.read_csv(path)
data_speed = drive_data["Speed"]
data_time = drive_data['Time']
sum_time = data_time.sum()

#max speed
max_speed = data_speed.max()
print(f'Max speed:',max_speed)
#min speed
min_speed = data_speed.min()
print(f'Min speed:',min_speed)
#average speed
average_speed = data_speed.mean()
print(f'Average speed:', average_speed)
#distance traveled
distance_traveled = data_speed.mean()/sum_time
print(f'Distance traveled:', distance_traveled)
#total time
print(f'Total time:', sum_time)