import numpy as np
import cv2
from is_msgs.image_pb2 import Image

def toNumpy(input_image):
    if isinstance(input_image, np.ndarray):
        output_image = input_image
    elif isinstance(input_image, Image):
        buffer = np.frombuffer(input_image.data, dtype = np.uint8)
        output_image = cv2.imdecode(buffer, flags = cv2.IMREAD_COLOR)
    else:
        output_image = np.array([], dtype = np.uint8)
    return output_image