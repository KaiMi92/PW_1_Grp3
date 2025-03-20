# Franks Versuche :)
import cv2
import numpy as np
import math

# def calculate_steering_angle(image, lines):
#     return 45
def calculate_steering_angle(image, lines):
    winkel_liste = [0]
    steering_angle = 90
    fahrwinkel_median = 0

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
        
#         # Berechnung der Steigung
        if (x2 - x1) != 0:
            slope = (y2 - y1) / (x2 - x1)
            angle_rad = np.arctan(slope)
            angle_deg = np.degrees(angle_rad) 
        else:
            slope = float('inf') 

        #print(f"Linie von ({x1},{y1}) nach ({x2},{y2}) hat eine Steigung von {slope}, Winkel {angle_deg}")
              
        winkel_liste.append(angle_deg)
        
        winkel_liste.sort()

        fahrwinkel_median = np.median(winkel_liste)
        steering_angle = (90-(fahrwinkel_median/2))
   
    return steering_angle