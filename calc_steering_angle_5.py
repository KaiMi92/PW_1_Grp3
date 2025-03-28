from model_container import ModelContainer
import numpy as np
import cv2

IMAGE_SIZE = (128, 128)
mc = ModelContainer("models/TFLite_Modell_Frank.tflite")

def calculate_steering_angle(image, lines):
    img_crop = cv2.resize(image, IMAGE_SIZE)
    img_crop = img_crop / 255.0
    img_crop = np.float32(img_crop)

    image_expanded = np.expand_dims(img_crop, axis=0)

    mc.interpreter.set_tensor(mc.input_details[0]["index" ], image_expanded)
    mc.interpreter.invoke()

    angle = mc.interpreter.get_tensor(mc.output_details[0]["index"])
    return angle