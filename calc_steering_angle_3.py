#from line_chart import *
# RS-Werte (30 - 110), (106 - 150), (26 - 86)
def calculate_steering_angle(image, lines):
    sum = 0
    runs = 0
    average = 0
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            # Berechnung der Steigung
            if (x2 - x1) != 0:
                slope = (y2 - y1) / (x2 - x1)
            else:
                continue
            #print(slope)
            runs += 1
            sum += slope
            average = sum/runs
        #print(average)

    x = 90
    if average > 0 and average <3:
        x = x - (average * 70)
        if x < 45:
            x = 45
            #print("Maximum Lenkwinkel von 45 Grad erreicht")
    elif average < 0 and average > -3:
        x = x + (abs(average) * 70)
        if x > 135:
            x = 135
            #print("Maximum Lenkwinkel von 135 Grad erreicht")
    #print(x)
    steering_angle = x
    return steering_angle

#calculate_steering_angle()