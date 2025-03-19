import cv2
import numpy as np
import math

# https://www.gutefrage.net/frage/wie-berechne-ich-abstand-von-punkt-und-gerade-allgemein2d
def distance_point_to_line(x1, y1, x2, y2, x0, y0):
    # Berechne den Abstand des Punktes von der Geraden
    numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denominator = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
    distance = numerator / denominator
    return distance

def calc_slope(x1, y1, x2, y2):
    if (x2 - x1) != 0:
        slope = (y2 - y1) / (x2 - x1)
    else:
        slope = float('inf') 
    return slope

def calculate_angle_alpha(image, x1, y1, x2, y2, x3, y3):
    # Berechne die Seitenlängen des Dreiecks
    # Reihenfolge: Pos Fahrzeug, Schnittpunkt, Geradeauspunkt 
    a = math.sqrt((x2 - x3)**2 + (y2 - y3)**2)  # Länge der Ankathete
    b = math.sqrt((x1 - x3)**2 + (y1 - y3)**2)  # Länge der Gegenkathete
    c = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)  # Länge der Hypotenuse

    cv2.line(image, (x1, y1), (x2, y2), (255, 255, 0), 1)
    cv2.line(image, (x2, y2), (x3, y3), (255, 255, 0), 1)
    cv2.line(image, (x3, y3), (x1, y1), (255, 255, 0), 1)

    
    print(f"Ankathete a = {a}")
    print(f"Gegenkathete b = {b}")
    print(f"Hypotenuse c = {c}")

    # Berechne den Winkel Alpha in Grad
    alpha = math.degrees(math.atan(b / a))

    # Der Winkel ist per Berechnung immer positiv
    # Wenn das Fahrzeug aber nach rechts fahren soll,
    # muss das Egebnis ein negativen Winkel sein
    if x2 > x3:
        alpha = -alpha

    print(f"alpha = {alpha}")    
    return alpha

def intersection_point(line1, line2):
    # print(f"Line1 = {line1}, type = {type(line1)}")
    # print(f"Line2 = {line2}, type = {type(line2)}")
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    # Berechne die Steigungen
    m1 = calc_slope(x1, y1, x2, y2)
    m2 = calc_slope(x3, y3, x4, y4)
    
    # Berechne die y-Achsenabschnitte
    b1 = y1 - m1 * x1
    b2 = y3 - m2 * x3
    
    # Berechne den Schnittpunkt
    if (m1 - m2) != 0:
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
    else:
        x = 0
        y = 0
    
    return int(x), int(y)

def calculate_steering_angle(image, lines):
    height, width, channels = image.shape
    nearest_neg_slope = 1000.0
    nearest_pos_slope = 1000.0
    nearest_neg_line = None
    nearest_pos_line = None

    # Koordinaten des Fahrzeug-Standortes
    xs = int(width / 2)
    ys = height
    
    # imageshape = (250, 640, 3)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            m = calc_slope(x1, y1, x2, y2)
            distance_to_car = distance_point_to_line(x1, y1, x2, y2, xs, ys)
            # print(f"Line P1({x1}|{y1}), P2({x2}|{y2}) - m={m}, distance = {distance_to_car} ")

            if m <= 0.0:
                # check for lines with negative slope
                if distance_to_car < nearest_neg_slope:
                    nearest_neg_slope = distance_to_car
                    nearest_neg_line = line[0]
            else:
                # check for lines with positive slope
                if distance_to_car < nearest_pos_slope:
                    nearest_pos_slope = distance_to_car
                    nearest_pos_line = line[0]


    if nearest_neg_line is not None:
        print("Draw nearest_neg_line")
        draw_line(image, nearest_neg_line, (0,0,200), 3)

    if nearest_pos_line is not None:
        print("Draw nearest_pos_line")
        draw_line(image, nearest_pos_line, (0,0,200), 3)

    if (nearest_neg_line is None) or (nearest_pos_line is None):
        if (nearest_neg_line is None) and (nearest_pos_line is None):
            print("No lines detected.")
            return 90
        else:
            print("Only one line detected.")
            one_line = nearest_neg_line
            if one_line is None:
                one_line = nearest_pos_line

            xi, yi = intersection_point(one_line, np.array([0, 0, 1, 0]))
    else:
        xi, yi = intersection_point(nearest_neg_line, nearest_pos_line)

    print(f"Schnittpunkt = ({xi}|{yi})")
    cv2.line(image, (xs, ys), (xi, yi), (255, 0, 0), 2)


    # Winkelberechnung GERADEAUS und Schnittpunkt beider Gerade
    # Rechwinkliges Dreieck aus Standort P_s, VirtuellerPunkt-GERADEAUS P_v und Schnittpunkt P_i
    xv = xs
    yv = yi

    steering_angle_float = calculate_angle_alpha(image, xs, ys, xi, yi, xv, yv)

    if math.isnan(steering_angle_float):
        steering_angle = 90
    else:
        steering_angle = int(steering_angle_float)
        
    print(f"steering_angle = {steering_angle}")



    # print(lines)

    # hier bitte jeder seine berechnung
    # steering_angle : int
    # steering angle of the car in degrees.
    # 90 degrees means straight forward
    # max. left steering angle is 135
    # max. right steering angle is 45
    return steering_angle

def draw_line(image, line, color, thickness):
    x1, y1, x2, y2 = line
    cv2.line(image, (x1, y1), (x2, y2), color, thickness)
