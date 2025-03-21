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
            winkel_liste.append(angle_deg)
        else:
            slope = float('inf') 

        #print(f"Linie von ({x1},{y1}) nach ({x2},{y2}) hat eine Steigung von {slope}, Winkel {angle_deg}")
              
        
        
        winkel_liste.sort()

        fahrwinkel_median = np.median(winkel_liste)

        if 0 <= fahrwinkel_median <= 15:
            steering_angle = 45
            print("Max-Links genommen")

        elif -15<= fahrwinkel_median < 0:
            steering_angle = 135
            print("Max-Rechts")
        else:
            steering_angle = (90-(fahrwinkel_median/2))
       

        
        print(f"Lenkwinkel= {steering_angle}")
        print(f"MedianWinkel= {fahrwinkel_median}")
        print(f"Winkel-Liste {winkel_liste}")
   
    return steering_angle