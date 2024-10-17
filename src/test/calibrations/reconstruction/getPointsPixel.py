from cameraParameters import LoadCameraParameters
import numpy as np
import cv2
import math
#sys.path.append(os.path.abspath(''))
# Pasta dos Arquivos
configPath = 'src/test/calibrations/'
imagePath = 'src/test/images/camera/'

cameraList = [1, 2, 4]
points = {
    'bola': {},
    'frente': {}
}
# Parâmetros das Câmeras
def LoadParameters(parameters: list) -> list:
    for id in range(1, 5):
        name = f'camera{id}'
        json = configPath+name+'.json'
        params = LoadCameraParameters(json, id)
        parameters.append(params)
    return parameters

parameters = LoadParameters([None])

def getxy(event, x, y, flags, param):
   global a 
   if event == cv2.EVENT_LBUTTONDOWN:
      a = np.vstack([a, np.hstack([x,y])])

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

# Exemplo 2: Pixel para ponto no mundo
def example2(parameters: list, show: bool = False) -> list:
    global a
    # P, u de cada câmera
    P = [None]
    U = [None]

    for id in cameraList:
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

        P.append(newK @ Rtcw)

        # # # Exemplo com bola vermelha
        # # Exemplo com frente
        # if id == 1:
        #     #U.append(np.array([[352], [175], [1]]))
        #     U.append(np.array([[360], [181], [1]]))
        # elif id == 2:
        #     #U.append(np.array([[651], [195], [1]]))
        #     U.append(np.array([[639], [203], [1]]))
        # Área de interesse
        dst = dst[y:y+h, x:x+w, :]
        if show:
            a = np.empty((0, 2))
            cv2.imshow(name, dst)
            cv2.setMouseCallback(name, getxy)
            cv2.waitKey(0)
            points['bola'][id] = (a[0][0], a[0][1])
            points['frente'][id] = (a[1][0], a[1][1])
    return P, U

P, U = example2(parameters, True)
print(points)
A = []
# for id in cameraList:
#     name = f'camera{id}'
#     #print(name)
#     #print(f'P{id}: ', P[id])
#     #print(f'U{id}: ', U[id])
#     #print()
#     zeros = np.zeros((3, 1))
#     mtx = np.array(P[id])
#     # print(mtx)
#     # print(U[id])
#     for i in range(len(cameraList)):
#         if i == id - 1:
#             mtx = np.hstack((mtx, -U[id]))
#         else:
#             mtx = np.hstack((mtx, zeros))
#     if len(A) == 0:
#         A = mtx
#     else:
#         A = np.vstack((A,mtx))
    
# #print('A', A)

# U, Sigma, V_transpose = np.linalg.svd(A)
# J = V_transpose[-1]
# J = J / J[3]

# #print('J', J)
# #example1(parameters, True)

# points = {
#     'bola': {
#         'x': -0.92168991,
#         'y': -1.11927853,
#         'z': 0.0626691
#     },
#     'frente': {
#         'x': -0.93933861,
#         'y': -0.90024259,
#         'z': 0.06643857
#     }
# }

# bola = [points['bola']['x'], points['bola']['y'], points['bola']['z']]
# frente = [points['frente']['x'], points['frente']['y'], points['frente']['z']]

# vector = np.subtract(frente, bola)

# print('Vetor:', vector)

# graus = math.degrees(math.atan2(vector[1],vector[0]))

# print('Ângulo:', graus)

# example2(parameters, True)