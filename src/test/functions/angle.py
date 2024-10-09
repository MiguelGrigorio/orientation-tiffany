import numpy as np
import math

def angle(center_body,  center_point, x_global):
    x = center_body[0] - center_point[0]
    y = -(center_body[1] - center_point[1])

    sen = y/np.sqrt(x**2 + y**2)
    cos = x/np.sqrt(x**2 + y**2)
    tan = sen/cos

    vector = np.array([x, y])
    vector = vector / np.linalg.norm(vector)
    angle = math.acos(np.dot(vector, x_global))
    angle = math.degrees(angle)

    if sen > 0 and cos > 0:
        pass
    elif sen > 0 and cos < 0:
        angle += 90
    elif sen < 0 and cos < 0:
        angle += 180
    elif sen < 0 and cos > 0:
        angle += 270
    return angle