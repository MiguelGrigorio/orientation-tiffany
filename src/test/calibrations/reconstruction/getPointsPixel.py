from cameraParameters import LoadCameraParameters
import numpy as np
import cv2

expec_loc = (635, 350)
distancia = []
for i in range(0, 4):
    param = LoadCameraParameters(f'src/test/calibrations/camera{i}.json', i)

    K = param.K
    shape = param.res
    R = param.R
    T = param.T
    Xw = np.array([[0.0], [0.0], [0.0], [1.0]])
    Rtcw = np.concatenate([R, T], axis=1)

    Xc = Rtcw @ Xw
    u = K @ Xc
    z = u[2]

    u = u / z


    # print('Xc:', Xc)
    # print('shape:', shape)
    # print('u:', u)
    # print('z:', z)

    loc = (int(u[0]), int(u[1]))

    path_image = 'src/test/images/camera/image.jpg'
    image = cv2.imread(path_image)
    image = cv2.resize(image, (1288, 728), image)

    # cv2.circle(image, loc, 10, (0, 0, 255), -1)
    # cv2.imshow('image', image)
    # cv2.waitKey(0)

    dist = np.linalg.norm(np.array(loc) - np.array(expec_loc))
    distancia.append(dist)   

print(distancia)