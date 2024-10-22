import cv2
import numpy as np

def world2pixel(dst: np.ndarray, newK: np.array, Rtcw: np.array, Xw: np.array, show: bool = False) -> None:
    Xc = Rtcw @ Xw
    u = newK @ Xc
    z = u[2]
    u = u / z

    loc = (int(u[0][0]), int(u[1][0]))

    if show:
        cv2.circle(dst, loc, 10, (0, 0, 255), -1)
        cv2.imshow("Ponto global", dst)
        cv2.waitKey(0)
