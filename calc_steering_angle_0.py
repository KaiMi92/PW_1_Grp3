import cv2
import numpy as np
import math

def draw_line(image, line, color, thickness):
    x1, y1, x2, y2 = line
    cv2.line(image, (x1, y1), (x2, y2), color, thickness)

# Copilot Berechnung
# 

def calculate_steering_angle(image, line_segments):
    height, width, _ = image.shape
    if line_segments is None:
        return 90  # Default steering angle if no line segments are detected
    
    left_fit = []
    right_fit = []
    
    for segment in line_segments:
        for x1, y1, x2, y2 in segment:
            if x1 == x2:
                continue  # Ignore vertical lines
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
    
    left_fit_average = np.average(left_fit, axis=0) if left_fit else None
    right_fit_average = np.average(right_fit, axis=0) if right_fit else None
    
    print(f"left_fit_average = {left_fit_average}")
    print(f"right_fit_average = {right_fit_average}")

    if left_fit_average is not None and right_fit_average is not None:
        left_slope, left_intercept = left_fit_average
        right_slope, right_intercept = right_fit_average
        mid = width // 2
        left_x = (height - left_intercept) / left_slope
        right_x = (height - right_intercept) / right_slope
        mid_x = (left_x + right_x) / 2
        angle_to_mid_radian = np.arctan((mid_x - mid) / height)
        angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / np.pi)

        print(f"left_x = {left_x}")
        print(f"right_x = {right_x}")
        print(f"mid_x = {mid_x}")
        print(f"angle_to_mid_deg = {angle_to_mid_deg}")

        return 90 + angle_to_mid_deg
    elif left_fit_average is not None:
        left_slope, left_intercept = left_fit_average
        left_x = (height - left_intercept) / left_slope
        angle_to_mid_radian = np.arctan((left_x - width // 2) / height)
        angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / np.pi)
        print(f"left_x = {left_x}")
        print(f"angle_to_mid_deg = {angle_to_mid_deg}")
        return 90 + 90 + angle_to_mid_deg
    elif right_fit_average is not None:
        right_slope, right_intercept = right_fit_average
        right_x = (height - right_intercept) / right_slope
        angle_to_mid_radian = np.arctan((right_x - width // 2) / height)
        angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / np.pi)
        print(f"right_x = {right_x}")
        print(f"angle_to_mid_deg = {angle_to_mid_deg}")
        return 90 + 90 + angle_to_mid_deg
    else:
        return 90  # Default steering angle if no line segments are detected

def calculate_steering_angle__(image, lines):
    if lines is None:
        return -90  # No lines detected, turn left as a default
    height, width, _ = image.shape
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_points(image, left_fit_average)
    right_line = make_points(image, right_fit_average)
    mid = int(width / 2)

    print(f"left_fit_average = {left_fit_average}")
    print(f"right_fit_average = {right_fit_average}")
    print(f"left_line = {left_line}")
    print(f"right_line = {right_line}")
    
    draw_line(image, left_line, (0,0,200), 2)
    draw_line(image, right_line, (0,0,200), 2)

    x_offset = ((left_line[2] + right_line[2]) / 2) - mid
    y_offset = int(height / 2)
    angle_to_mid_radian = np.arctan(x_offset / y_offset)
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / np.pi)
    steering_angle = angle_to_mid_deg + 90 + 90

    print(f"angle_to_mid_deg = {angle_to_mid_deg}")
    print(f"steering_angle = {steering_angle}")

    return steering_angle

def make_points(image, line):
    height, width, _ = image.shape
    slope, intercept = line
    y1 = height
    y2 = int(y1 * 0.6)
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return [x1, y1, x2, y2]

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)
    return line_image