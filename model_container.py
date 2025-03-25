import tflite_runtime.interpreter as tflite
from tflite_runtime.interpreter import Interpreter

IMAGE_SIZE = (128, 128)

class ModelContainer():
    def __init__(self, path):
        # Load the TFLite model
        self.interpreter = Interpreter(model_path=path)
        self.interpreter.allocate_tensors()

        # Get input and output tensors
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # Rechnekapazität reservieren
        self.interpreter.allocate_tensors()