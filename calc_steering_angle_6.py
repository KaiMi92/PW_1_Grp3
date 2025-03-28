from model_container import ModelContainer
import numpy as np
import cv2
from image_size import IMAGE_SIZE
from datetime import datetime
from software.basisklassen_cam import *

model_name = "models/industrious-foal-67.tflite"
model_name = "models/unruly-steed-640.tflite"
model_name = "models/aged-snail-344.tflite"
model_name = "models/vaunted-foal-169.tflite"
model_name = "models/honorable-fox-708.tflite"
model_name = "models/caring-lynx-1000_bw.tflite"


mc = ModelContainer(model_name)

def calculate_steering_angle(image, lines):
    print(f"Use model {model_name}, image.shape = {image.shape}")

    # img_crop = image[150:350,:,:]
    img_crop = image[100:400,:,:]
    img_crop = cv2.resize(img_crop, IMAGE_SIZE)

    if model_name == "models/caring-lynx-1000_bw.tflite":
        # Use the cvtColor() function to grayscale the image
        img_crop = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)

    # Save image
    # curr_time = datetime.now()
    # timestr = curr_time.strftime('%Y-%m-%d_%H-%M-%S.%f')
    # filename = './nn_cropped_img/car_img_' + timestr + '.jpg'
    # cv2.imwrite(filename, img_crop)

    img_crop = img_crop / 255.0
    img_crop = np.float32(img_crop)

    if model_name == "models/caring-lynx-1000_bw.tflite":
        img_crop = np.expand_dims(img_crop, axis=-1)


    image_expanded = np.expand_dims(img_crop, axis=0)

    mc.interpreter.set_tensor(mc.input_details[0]["index" ], image_expanded)
    mc.interpreter.invoke()

    angle = mc.interpreter.get_tensor(mc.output_details[0]["index"])

    print(f"NN2 angle = {angle}")
    return int(angle)

if __name__ == "__main__":
    cam = Camera()
    img = cam.get_frame()
    # img = cv2.imread('img/car_img_2025-03-25_10-51-48.275981_118.jpg') 
    # img = cv2.imread('img/car_img_2025-03-27_14-57-47.656899_113.jpg') 
    # img = cv2.imread('use_these_images/aug0ccar_img_2025-03-24_15-53-49.278022_80.jpg')
    print(img.shape)
    
    angle = calculate_steering_angle(img, None)
    print(f"angle = {angle}")