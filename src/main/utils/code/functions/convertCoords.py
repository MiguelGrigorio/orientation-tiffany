import cv2
import numpy as np

def undistort(parameters: list, imagePath: str, selectCameras: list) -> list:
    # P de cada câmera (newK @ Rtcw)
    P = [None]
    distort = [None]
    interestArea = [None]
    newKs = [None]
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

        image = cv2.imread(imagePath + name + '.jpg')

        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        w, h = res

        # Corrige a matriz K para levar em consideração a nova imagem sem disorção
        newK, roi = cv2.getOptimalNewCameraMatrix(K, dis, res, 1, res)

        dst = cv2.undistort(img, K, dis, None, newK)
        
        dst = cv2.cvtColor(dst, cv2.COLOR_RGB2BGR)

        x, y, w, h = roi
        newK[0, 2] = newK[0, 2] - x
        newK[1, 2] = newK[1, 2] - y

        # Área de interesse
        roi = dst[y:y+h, x:x+w, :]
        P.append(newK @ Rtcw)
        distort.append(dst)
        interestArea.append(roi)
        newKs.append(newK)

    return P, distort, interestArea, newKs

def world2pixel(parameters: list, imagePath: str, selectCameras: list, Xw: np.array, show: bool = False) -> list[tuple]:
    _, _, image, newKs = undistort(parameters, imagePath, selectCameras)
    locs = []
    for id in [1, 2, 3, 4]:
        if not id in selectCameras:
            locs.append(None)
            continue
        Rtcw = parameters[id].Rtcw
        Xc = Rtcw @ Xw
        u = newKs[id] @ Xc
        z = u[2]
        u = u / z

        loc = [int(u[0][0]), int(u[1][0])]
        locs.append(loc)
        if show:
            cv2.circle(image[id], loc, 10, (0, 0, 255), -1)
            cv2.imshow("Ponto global", image[id])
            cv2.waitKey(0)
    return locs

def pixel2world(parameters: list, imagePath: str, selectCameras: list, locs: list) -> np.array:
    P, _, _, _ = undistort(parameters, imagePath, selectCameras)
    # mtxU é a localização do ponto em cada câmera em pixels
    # mtxP é newK @ Rtcw
    # mtxA é a matriz para resolver o sistema de equações com svd
    # exemplo: mtxA = [P1 -u1 zeros; P2 zeros -u2]
    # Xw é o ponto global

    u = locs
    A = []
    for id in [1, 2, 3, 4]:
        if not id in selectCameras:
            continue
        zeros = np.zeros((3, 1))
        mtx = np.array(P[id])

        # Cada linha

        for i in selectCameras:
            if i == id:
                mtx = np.hstack((mtx, -u[id]))
            else:
                mtx = np.hstack((mtx, zeros))
        # Formando a matriz A
        if len(A) == 0:
            A = mtx
        else:
            A = np.vstack((A, mtx))

    _, _, V_transpose = np.linalg.svd(A)
    V = V_transpose[-1]
    V = V / V[3]
    Xw = V[:3]
    return Xw