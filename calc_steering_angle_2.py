import cv2
import numpy as np
import math

# https://www.gutefrage.net/frage/wie-berechne-ich-abstand-von-punkt-und-gerade-allgemein2d
def distance_point_to_line(x1, y1, x2, y2, x0, y0):
    # Berechne den Abstand des Punktes von der Geraden
    numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denominator = np.sqrt((y2 - y1)**2 + (x2 - x1)**2)
    distance = numerator / denominator
    return distance

def y_distance_to_car(x1, y1, x2, y2, x0, y0):
    return min((y0 - y1), (y0 - y2))

def x_distance_to_car(x1, y1, x2, y2, x0, y0):
    return abs(x0-x2)

def calc_slope(x1, y1, x2, y2):
    if (x2 - x1) != 0:
        slope = (y2 - y1) / (x2 - x1)
    else:
        slope = float('inf') 
    return slope

def calculate_angle_alpha(image, x1, y1, x2, y2, x3, y3):
    # Berechne die Seitenlängen des Dreiecks
    # Reihenfolge: Pos Fahrzeug, Schnittpunkt, Geradeauspunkt 
    a = np.sqrt((x2 - x3)**2 + (y2 - y3)**2)  # Länge der Ankathete
    b = np.sqrt((x1 - x3)**2 + (y1 - y3)**2)  # Länge der Gegenkathete
    c = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)  # Länge der Hypotenuse

    cv2.line(image, (x1, y1), (x2, y2), (255, 255, 0), 1)
    cv2.line(image, (x2, y2), (x3, y3), (255, 255, 0), 1)
    cv2.line(image, (x3, y3), (x1, y1), (255, 255, 0), 1)

    
    print(f"Ankathete a = {a}")
    print(f"Gegenkathete b = {b}")
    print(f"Hypotenuse c = {c}")

    # Berechne den Winkel Alpha in Grad
    if a != 0:
        alpha = np.degrees(np.arctan(b / a))
    else:
        alpha = 90

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
    
    if np.isnan(x):
        x = 0
    
    if np.isnan(y):
        y = 0
    
    return int(x), int(y)


def calculate_angle_by_slope(slope):
    # Berechne den Winkel in Radiant
    angle_radians = np.arctan(abs(slope))
    
    # Konvertiere den Winkel in Grad
    angle_degrees = np.degrees(angle_radians)
    
    return angle_degrees

def curve_is_too_tight(xs, ys, nearest_neg_line, nearest_pos_line, slope_of_nearest_neg_line, slope_of_nearest_pos_line):
    threshhold_slope = 0.1
    upper_threshhold_distance = 100
    lower_threshhold_distance = 10

    if (nearest_neg_line is None) and (nearest_pos_line is None):
        return False
    
    if (nearest_neg_line is None):
        x1, y1, x2, y2 = nearest_pos_line
        d_pos = distance_point_to_line(x1, y1, x2, y2, xs, ys)

        print(f"Distance from pos P_S = {d_pos}")
        if d_pos > upper_threshhold_distance:
            return False
        
        if d_pos < lower_threshhold_distance:
            return True

        return (abs(slope_of_nearest_pos_line) < threshhold_slope)
    
    if (nearest_pos_line is None):
        x1, y1, x2, y2 = nearest_neg_line
        d_neg = distance_point_to_line(x1, y1, x2, y2, xs, ys)

        print(f"Distance from neg P_S = {d_neg}")
        if d_neg > upper_threshhold_distance:
            return False

        if d_neg < lower_threshhold_distance:
            return True

        return (abs(slope_of_nearest_neg_line) < threshhold_slope)

    x1, y1, x2, y2 = nearest_pos_line
    d_pos = distance_point_to_line(x1, y1, x2, y2, xs, ys)

    x1, y1, x2, y2 = nearest_neg_line
    d_neg = distance_point_to_line(x1, y1, x2, y2, xs, ys)

    print(f"Distance from pos P_S = {d_pos}")
    print(f"Distance from neg P_S = {d_neg}")

    if min(d_neg, d_pos) > upper_threshhold_distance:
        return False

    return (max(abs(slope_of_nearest_neg_line), abs(slope_of_nearest_pos_line)) < threshhold_slope)


def calculate_steering_angle(image, lines):
    height, width, channels = image.shape
    slope_of_nearest_neg_line = 1000.0
    slope_of_nearest_pos_line = 1000.0
    y_dist_of_nearest_neg_line = 1000.0
    y_dist_of_nearest_pos_line = 1000.0
    x_dist_of_nearest_neg_line = 1000.0
    x_dist_of_nearest_pos_line = 1000.0
    nearest_neg_line = None
    nearest_pos_line = None
    curve_is_too_tight_factor = 1

    # Koordinaten des Fahrzeug-Standortes
    xs = int(width / 2)
    ys = height
    
    # imageshape = (250, 640, 3)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            m = calc_slope(x1, y1, x2, y2)
            y_distance_to_car_tmp = y_distance_to_car(x1, y1, x2, y2, xs, ys)
            x_distance_to_car_tmp = x_distance_to_car(x1, y1, x2, y2, xs, ys)
            # print(f"Line P1({x1}|{y1}), P2({x2}|{y2}) - m={m}, distance = {distance_to_car} ")

            if m <= 0.0:
                # check for lines with negative slope
                if y_distance_to_car_tmp < y_dist_of_nearest_neg_line:
                    y_dist_of_nearest_neg_line = y_distance_to_car_tmp
                    x_dist_of_nearest_neg_line = x_distance_to_car_tmp
                    slope_of_nearest_neg_line = m
                    nearest_neg_line = line[0]
            else:
                # check for lines with positive slope
                if y_distance_to_car_tmp < y_dist_of_nearest_pos_line:
                    y_dist_of_nearest_pos_line = y_distance_to_car_tmp
                    x_dist_of_nearest_pos_line = x_distance_to_car_tmp
                    slope_of_nearest_pos_line = m
                    nearest_pos_line = line[0]


    print(f"y-Distances: Left = {y_dist_of_nearest_neg_line}, Right = {y_dist_of_nearest_pos_line}")

    # remove lines that are far away
    if y_dist_of_nearest_neg_line - y_dist_of_nearest_pos_line > 75:
        print("y-remove left line!")
        nearest_neg_line = None
    elif y_dist_of_nearest_pos_line - y_dist_of_nearest_neg_line > 75:
        print("y-remove right line!")
        nearest_pos_line = None

    print(f"x-Distances: Left = {x_dist_of_nearest_neg_line}, Right = {x_dist_of_nearest_pos_line}")
    # remove lines that are far away
    if x_dist_of_nearest_neg_line - x_dist_of_nearest_pos_line > 75:
        print("x-remove left line!")
        nearest_neg_line = None
    elif x_dist_of_nearest_pos_line - x_dist_of_nearest_neg_line > 75:
        print("x-remove right line!")
        nearest_pos_line = None

    if nearest_neg_line is not None:
        draw_line(image, nearest_neg_line, (0,0,200), 2)

    if nearest_pos_line is not None:
        draw_line(image, nearest_pos_line, (0,0,200), 2)

    # check tight curves
    if curve_is_too_tight(xs, ys, nearest_neg_line, nearest_pos_line, slope_of_nearest_neg_line, slope_of_nearest_pos_line):
        print(f"Curve is too tight, mn = {slope_of_nearest_neg_line}, mp = {slope_of_nearest_pos_line}")
        curve_is_too_tight_factor = -1

    # print(f"nearest_neg_slope = {slope_of_nearest_neg_line}, nearest_pos_slope  = {slope_of_nearest_pos_line}")

    if (nearest_neg_line is None) or (nearest_pos_line is None):
        if (nearest_neg_line is None) and (nearest_pos_line is None):
            print("No lines detected.")
            return 90
        else:
            one_line = nearest_neg_line
            slope = slope_of_nearest_neg_line
            if one_line is None:
                one_line = nearest_pos_line
                slope = slope_of_nearest_pos_line

            steering_angle_float = calculate_angle_by_slope(-slope)
            if slope > 0:
                steering_angle_float = 90.0 - steering_angle_float
            else:
                steering_angle_float = 90.0 + steering_angle_float

            if np.isinf(slope):
                # slope = 999999999.0
                steering_angle_float = np.nan

            print(f"Only one line detected, m = {slope}, alpha = {steering_angle_float}")
            if np.isnan(steering_angle_float):
                steering_angle = 90
            else:
                steering_angle = int(steering_angle_float)
    else:
        xs_dist_left, _ = intersection_point(nearest_neg_line, np.array([xs, ys, 0, ys]))
        xs_dist_left = abs(xs - xs_dist_left)

        xs_dist_right, _ = intersection_point(nearest_pos_line, np.array([xs, ys, 0, ys]))
        xs_dist_right = abs(xs_dist_right - xs)

        rel = xs_dist_left / (xs_dist_left + xs_dist_right)

        lower_limit = 0.2
        upper_limit = 0.8
        limit_diff = upper_limit - lower_limit

        if rel < lower_limit:
            steering_angle = 45
        elif rel > upper_limit:
            steering_angle = 135
        else:
            # lower_limit = Linker Ausschlag = 0
            # upper_limit = Rechter Ausschlag = 90
            rel_diff = rel * limit_diff
            steering_angle = 90 * rel_diff / limit_diff
            steering_angle = steering_angle + 45
    
            # steering_angle = 90 * (1 - rel) + 45
            print(f"xs_dist_left = {xs_dist_left}, xs_dist_right = {xs_dist_right}, rel = {rel}, limit_diff = {limit_diff}, rel_diff = {rel_diff}, steering_angle = {steering_angle}")
        
        print(f"xs_dist_left = {xs_dist_left}, xs_dist_right = {xs_dist_right}, steering_angle = {steering_angle}")

    return curve_is_too_tight_factor * steering_angle

def draw_line(image, line, color, thickness):
    x1, y1, x2, y2 = line
    cv2.line(image, (x1, y1), (x2, y2), color, thickness)
