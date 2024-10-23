from utils.code.classes.LoadCameraParameters import LoadCameraParameters
from utils.code.functions.angle import angle
from utils.code.getImages import getImages
from utils.code.functions.convertCoords import world2pixel, undistort, pixel2world
import numpy as np
import cv2

selectCameras = [2]

configPath = 'etc/calibrations/'
tiffanyPath = 'assets/images/camera/'
cameraPath = 'assets/images/photos/'

#getImages(cameraPath, 1, selectCameras, True)

# Camera 2 roi = x, y, w, h
tiffany_2 = (620, 185, 55, 35)

# region Exemplo de pontos

points = {'bola': {1: (351.0, 172.0), 2: (650.0, 195.0), 4: (518.0, 308.0)}, 'frente': {1: (361.0, 181.0), 2: (639.0, 204.0), 4: (535.0, 294.0)}} # Pontos já selecionados
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

# region Testes

# Xw = np.array([[0.0], [0.0], [0.0], [1.0]])
# world2pixel(parameters, tiffanyPath, selectCameras, Xw, True)


# Basicamente o meu problema
# locs = [None]
# for id in [1, 2, 3, 4]:
#     if id not in selectCameras:
#         locs.append(None)
#         continue
#     p = np.array([[points['bola'][id][0]], [points['bola'][id][1]], [1]])
#     locs.append(p)

# Xws_bola = pixel2world(parameters, tiffanyPath, selectCameras, locs)

# locs = [None]
# for id in [1, 2, 3, 4]:
#     if id not in selectCameras:
#         locs.append(None)
#         continue
#     p = np.array([[points['frente'][id][0]], [points['frente'][id][1]], [1]])
#     locs.append(p)

# Xws_frente = pixel2world(parameters, tiffanyPath, selectCameras, locs)

# vector = np.subtract(Xws_frente[:2], Xws_bola[:2])
# vector = [float(vector[0]), float(vector[1])]
# vector = [round(vector[0], 2), round(vector[1], 2)]
# print('Vetor:', vector)
# graus = angle(vector)
# graus = round(graus, 2)
# print('Ângulo:', graus)
# endregion


# Tenho que fazer o contrário aqui, dividir pela proporção do resize, e somar o x e y do roi e teoricamente, teria o ponto correto no mundo
location = points['tiffany'][2]
_, _, roi, _ = undistort(parameters, tiffanyPath, selectCameras)
def tiffany(roi, image, location: list):
    x, y, w, h = roi
    newLoc = [location[0] - x, location[1] - y]
    return image[y:y+h, x:x+w, :], newLoc

Tiffany, newLoc = tiffany(tiffany_2, roi[2], location)
shape = Tiffany.shape
prop = 500 / shape[1]
newLoc = [int(newLoc[0] * prop), int(newLoc[1] * prop)]
Tiffany = cv2.resize(Tiffany, None, fx=prop, fy=prop)
cv2.circle(Tiffany, newLoc, 3, (255, 0, 255), -1)
cv2.imshow('Tiffany', Tiffany)
cv2.waitKey(0)

pointss = [None]
for id in [1, 2, 3, 4]:
    if id not in selectCameras:
        pointss.append(None)
        continue
    pp = np.array([[points['tiffany'][id][0]], [points['tiffany'][id][1]], [1]])
    pointss.append(pp)
p = pixel2world(parameters, tiffanyPath, selectCameras, pointss)
print(p)


# region Provisório para seleção de pontos

pixels = np.empty((0, 2))
def getxy(event, x, y, flags, param):
    global pixels
    if event == cv2.EVENT_LBUTTONDOWN:
        pixels = np.vstack([pixels, np.hstack([x,y])])
        cv2.destroyAllWindows()

def selectPoints(selectCameras: list):
    points = { 'bola': {}, 'frente': {} }
    _, _, roi, _ = undistort(parameters, tiffanyPath, selectCameras)
    for id in [1, 2, 3, 4]:
        if id not in selectCameras:
            continue

        name = f'Selecione o centro do ponto (Camera {id})'
        cv2.imshow(name, roi[id])
        cv2.setMouseCallback(name, getxy)
        while pixels.shape[0] < 1:
            cv2.waitKey(1)
        points['bola'][id] = (int(pixels[0][0]), int(pixels[0][1]))
        cv2.circle(roi[id], points['bola'][id], 3, (255, 0, 255), -1)

        name = f'Selecione a frente da Tiffany (Camera {id})'
        cv2.imshow(name, roi[id])
        cv2.setMouseCallback(name, getxy)
        while pixels.shape[0] < 2:
            cv2.waitKey(1)
        points['frente'][id] = (int(pixels[1][0]), int(pixels[1][1]))
        cv2.circle(roi[id], points['frente'][id], 3, (255, 255, 0), -1)

        name = f'Pontos selecionados (Camera {id})'
        cv2.imshow(name, roi[id])
        cv2.waitKey(0)
        pixels = np.empty((0, 2))
    return points

# endregion