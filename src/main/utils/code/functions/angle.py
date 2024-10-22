import numpy as np
import math

def angle(vector, x_global = [1, 0]):
    vector = vector / np.linalg.norm(vector)
    angle = math.acos(np.dot(vector, x_global))
    angle = math.degrees(angle)
    sen = vector[1]
    cos = vector[0]

    if sen > 0 and cos > 0 and angle <= 90:
        pass
    elif sen > 0 and cos < 0 and angle < 90:
        angle += 90
    elif sen < 0 and cos < 0 and angle <= 90:
        angle += 180
    elif sen < 0 and cos > 0 and angle < 90:
        angle += 270
    return angle