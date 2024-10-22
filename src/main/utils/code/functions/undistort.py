import cv2
import numpy as np

def undistort(parameters: list, imagePath: str, selectCameras: list) -> list:
    # P de cada câmera (newK @ Rtcw)
    P = [None]
    distort = [None]
    interestArea = [None]

    for id in [1, 2, 3 ,4]:             # Todas as câmeras
        if id not in selectCameras:
            P.append(None)
            distort.append(None)
            interestArea.append(None)
            continue
        name = f'camera{id}'
        params = parameters[id]
        K = params.K
        Rtcw = params.Rtcw
        res = params.res
        dis = params.dis

        image = cv2.imread(imagePath+name+'.jpg')

        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        w, h = res

        # Corrige a matriz K para levar em consideração a nova imagem sem disorção
        newK, roi = cv2.getOptimalNewCameraMatrix(K, dis, res, 1, res)

        dst = cv2.undistort(img, K, dis, None, newK)
        
        dst = cv2.cvtColor(dst, cv2.COLOR_RGB2BGR)

        x,y,w,h = roi
        newK[0, 2] = newK[0, 2] - x
        newK[1, 2] = newK[1, 2] - y

        # Área de interesse
        roi = dst[y:y+h, x:x+w, :]
        P.append(newK @ Rtcw)
        distort.append(dst)
        interestArea.append(roi)

    return P, distort, interestArea, newK