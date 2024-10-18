from utils.classes.LoadCameraParameters import LoadCameraParameters
from utils.functions.angle import angle
import numpy as np
import cv2

configPath = 'etc/calibrations/'
imagePath = 'assets/images/camera/'

cameraList = [1, 2, 3, 4]
selectCameras = [1, 2, 4]

'''
points = { 'bola': {}, 'frente': {} }
'''

points = {'bola': {1: (351.0, 172.0), 2: (650.0, 195.0), 4: (518.0, 308.0)}, 'frente': {1: (361.0, 181.0), 2: (639.0, 204.0), 4: (535.0, 294.0)}}

for where in points.keys():
    keys = list(points[where].keys())
    for id in keys:
        if id not in selectCameras:
            del points[where][id]

def LoadParameters(parameters: list) -> list:
    for id in range(1, 5):
        name = f'camera{id}'
        json = configPath+name+'.json'
        params = LoadCameraParameters(json, id)
        parameters.append(params)
    return parameters

parameters = LoadParameters([None])

pixels = np.empty((0, 2))

def getxy(event, x, y, flags, param):
    global pixels
    if event == cv2.EVENT_LBUTTONDOWN:
        pixels = np.vstack([pixels, np.hstack([x,y])])

# Exemplo 1: Ponto no mundo para pixel
def example1(parameters: list, show: bool = False) -> None:
    # Transformação de cada câmeraa
    for id in cameraList:
        name = f'camera{id}'
        params = parameters[id]
        K = params.K
        R = params.R
        T = params.T
        res = params.res
        dis = params.dis

        # Ponto no mundo
        Xw = np.array([[-2.02], [-3.07], [1.3], [1.0]]) 
        #Xw = np.array([[0.0], [0.0], [0.0], [1.0]]) 
        Rtcw = np.concatenate([R, T], axis=1)

        Xc = Rtcw @ Xw

        image = cv2.imread(imagePath+name+'.jpg')
        img = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

        w, h = res

        # Corrige a matriz K para levar em consideração a nova imagem sem disorção
        newK, roi = cv2.getOptimalNewCameraMatrix(K, dis,(w,h),1,(w,h))

        # print('Nova matriz K: ',newK)
        # print('K: ',K)

        dst = cv2.undistort(img, K, dis, None, newK)
        
        dst = cv2.cvtColor(dst, cv2.COLOR_RGB2BGR)

        x,y,w,h = roi
        newK[0, 2] = newK[0, 2] - x
        newK[1, 2] = newK[1, 2] - y
        u = newK @ Xc
        z = u[2]
        u = u / z

        loc = (int(u[0][0]), int(u[1][0]))

        dst = dst[y:y+h, x:x+w, :]
        if show:
            cv2.circle(dst, loc, 10, (0, 0, 255), -1)
            cv2.imshow(name, dst)
            cv2.waitKey(0)

def undistort(parameters: list) -> list:
    # P de cada câmera (newK @ Rtcw)
    P = [None]
    distort = [None]
    interestArea = [None]

    for id in cameraList:
        if id not in selectCameras:
            P.append(None)
            distort.append(None)
            interestArea.append(None)
            continue
        name = f'camera{id}'
        params = parameters[id]
        K = params.K
        R = params.R
        T = params.T
        res = params.res
        dis = params.dis

        Rtcw = np.concatenate([R, T], axis=1)

        image = cv2.imread(imagePath+name+'.jpg')

        img = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

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

    return P, distort, interestArea

P, dst, roi = undistort(parameters)
select = True if points['bola'] == {} else False
if select:
    for id in cameraList:
        if id not in selectCameras:
            continue
        name = f'camera{id}'
        image = cv2.imread(imagePath+name+'.jpg')
        cv2.imshow(name, roi[id])
        cv2.setMouseCallback(name, getxy)
        cv2.waitKey(0)
        points['bola'][id] = (pixels[0][0], pixels[0][1])
        points['frente'][id] = (pixels[1][0], pixels[1][1])
        pixels = np.empty((0, 2))

A = { 'bola': {}, 'frente': {} }
U = { 'bola': {}, 'frente': {} }

for where in points.keys():
    for id in points[where].keys():
        coordToU = np.array([[points[where][id][0]], [points[where][id][1]], [1]])

        try:
            U[where][id].append(coordToU)
        except:
            U[where][id] = [coordToU]

for where in U.keys():
    for id in selectCameras:
        zeros = np.zeros((3, 1))
        mtx = np.array(P[id])
        for i in U[where].keys():
            if i == id:
                mtx = np.hstack((mtx, -U[where][id][0]))
            else:
                mtx = np.hstack((mtx, zeros))
        if len(A[where]) == 0:
            A[where] = mtx
        else:
            A[where] = np.vstack((A[where], mtx))

vn = { 'bola': [], 'frente': [] }

for where in vn.keys():
    _, _, V_transpose = np.linalg.svd(A[where])
    vn[where] = V_transpose[-1]
    vn[where] = vn[where] / vn[where][3]

coord = { 'bola': [], 'frente': [] }

for where in vn.keys():
    for i in range(3):
        coord[where].append(vn[where][i])
vector = np.subtract(coord['frente'], coord['bola'])
vector = [vector[0], vector[1]]
print('Vetor:', vector)
graus = angle(vector)
print('Ângulo:', graus)