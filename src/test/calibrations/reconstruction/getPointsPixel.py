from utils.code.cameraParameters import LoadCameraParameters
import numpy as np
import cv2

# Pasta dos Arquivos
config_path = 'src/test/calibrations/'
image_path = 'src/test/images/camera/'

# Parâmetros das Câmeras

def LoadParameters (parameters: list = []) -> list:
    for id in range(1, 5):
        name = f'camera{id}'
        json = config_path+name+'.json'
        params = LoadCameraParameters(json, id)
        parameters.append(params)
        return parameters
parameters = LoadParameters()

# Transformação de cada câmera
for id in range(1, 5):
    name = f'camera{id}'
    json = config_path+name+'.json'
    params = LoadCameraParameters(json, id)

    K = params.K
    R = params.R
    T = params.T

    # Ponto esperado
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

    loc = (int(u[0][0]), int(u[1][0]))

  
    image = cv2.imread(image_path+name+'.jpg')

    cv2.circle(image, loc, 10, (0, 0, 255), -1)
    cv2.imshow(json, image)
    cv2.waitKey('q')