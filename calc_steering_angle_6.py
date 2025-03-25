from model_container import ModelContainer
import numpy as np
import cv2

IMAGE_SIZE = (128, 128)
mc = ModelContainer("TFLite_Modell_Sebastian.tflite")

def calculate_steering_angle(image, lines):
    img_crop = image[150:350,:,:]
    img_crop = cv2.resize(img_crop, IMAGE_SIZE)
    img_crop = img_crop / 255.0
    img_crop = np.float32(img_crop)

    image_expanded = np.expand_dims(img_crop, axis=0)

    mc.interpreter.set_tensor(mc.input_details[0]["index" ], image_expanded)
    mc.interpreter.invoke()

    angle = mc.interpreter.get_tensor(mc.output_details[0]["index"])
    return angle

if __name__ == "__main__":
    img = cv2.imread('img/car_img_2025-03-25_10-51-48.275981_118.jpg') 
    print(img.shape)
    

    img_crop = img[150:350,:,:]
    img_crop = cv2.resize(img_crop, IMAGE_SIZE)
    img_crop = img_crop / 255.0
    img_crop = np.float32(img_crop)

    angle = calculate_steering_angle(img_crop, None)
    print(f"angle = {angle}")