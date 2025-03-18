# %%
import cv2
import matplotlib.pyplot as plt
import numpy as np

# %%
path = "img/car_img_2025-03-18_10-53-51.131396.jpg"
img = cv2.imread(path)
plt.imshow(img)

# %%
plt.imshow(img[:, :, ::-1])

# %%
img_crop = img[100:350,:,:]
img_hsv = cv2.cvtColor(img_crop, cv2.COLOR_BGR2HSV)


# %%
lower_blue = np.array([100, 150, 0])
upper_blue = np.array([140, 255, 255])
mask = cv2.inRange(img_hsv, lower_blue, upper_blue)


# %%
edges = cv2.Canny(mask, 50, 150, apertureSize=3)


# %%
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)


# %%
line_img = img_crop.copy()

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)


# %%
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        
        # Berechnung der Steigung
        if (x2 - x1) != 0:
            slope = (y2 - y1) / (x2 - x1)
            angle_rad = np.arctan(slope)
            angle_deg = np.degrees(angle_rad) 
        else:
            slope = float('inf') 

        print(f"Linie von ({x1},{y1}) nach ({x2},{y2}) hat eine Steigung von {slope}, Winkel {angle_deg}")

# %%



