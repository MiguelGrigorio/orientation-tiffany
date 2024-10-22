from utils.code.classes.LoadCameraParameters import LoadCameraParameters
from utils.code.functions.angle import angle
from utils.code.getImages import getImages
from utils.code.functions.undistort import undistort
from utils.code.functions.convertCoords import world2pixel
import numpy as np
import cv2

cameraList = [1, 2, 3, 4]
selectCameras = cameraList

configPath = 'etc/calibrations/'
tiffanyPath = 'assets/images/camera/'
cameraPath = 'assets/images/photos/'

#getImages(cameraPath, 1, selectCameras, True)

# Camera 2 roi = x, y, w, h
tiffany_2 = (620, 185, 55, 35)

# region Exemplo de pontos
#points = { 'bola': {}, 'frente': {} } # Para selecionar os pontos
#points = {'bola': {1: (351.0, 172.0), 2: (650.0, 195.0), 4: (518.0, 308.0)}, 'frente': {1: (361.0, 181.0), 2: (639.0, 204.0), 4: (535.0, 294.0)}} # Pontos já selecionados
points = { 'tiffany': {2: (645, 200)} } # Próximo do centro da tiffany
# endregion

for where in points.keys():
    keys = list(points[where].keys())
    for id in keys:
        if id not in selectCameras:
            del points[where][id]

def LoadParameters(configPath: str) -> list:
    parameters = [None]
    for id in range(1, 5):
        name = f'camera{id}'
        json = configPath+name+'.json'
        params = LoadCameraParameters(json, id)
        parameters.append(params)
    return parameters

parameters = LoadParameters(configPath)

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
        #Xw = np.array([[-2.02], [-3.07], [1.3], [1.0]]) 
        Xw = np.array([[0.0], [0.0], [0.0], [1.0]]) 
        Rtcw = np.concatenate([R, T], axis=1)

        Xc = Rtcw @ Xw

        image = cv2.imread(tiffanyPath+name+'.jpg')
        img = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

        w, h = res

        # Corrige a matriz K para levar em consideração a nova imagem sem disorção
        newK, roi = cv2.getOptimalNewCameraMatrix(K, dis,(w,h),1,(w,h))

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

P, dst, roi, newK = undistort(parameters, tiffanyPath, selectCameras)
Xw = np.array([[0.0], [0.0], [0.0], [1.0]])


pixel = world2pixel(roi[2], newK, parameters[2].Rtcw, Xw, True)

cv2.circle(dst[2], pixel, 10, (0, 0, 255), -1)
cv2.imshow('tiffany', dst[2])
cv2.waitKey(0)


def tiffany(roi, image):
    x, y, w, h = roi
    return image[y:y+h, x:x+w, :]
tiffany = tiffany(tiffany_2, roi[2])
shape = tiffany.shape
prop = 500 / shape[1]

tiffany = cv2.resize(tiffany, None, fx=prop, fy=prop)
cv2.imshow('tiffany', tiffany)
cv2.waitKey(0)


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