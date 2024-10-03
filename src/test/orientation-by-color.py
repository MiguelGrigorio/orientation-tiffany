import cv2
import numpy as np
import math

def color(point: tuple, body: tuple, lower_threshold: float, upper_threshold: float):
    # RGB para BGR
    body = (body[2], body[1], body[0])
    point = (point[2], point[1], point[0])

    # Intervalo de cor
    color = {
        "body": {
            "lower": np.array([body[0] * lower_threshold, body[1] * lower_threshold, body[2] * lower_threshold]),
            "upper": np.array([body[0] * upper_threshold, body[1] * upper_threshold, body[2] * upper_threshold])
            },
        "point": {
            "lower": np.array([point[0] * lower_threshold, point[1] * lower_threshold, point[2] * lower_threshold]),
            "upper": np.array([point[0] * upper_threshold, point[1] * upper_threshold, point[2] * upper_threshold])
        }
    }
    return color
def orient_by_color(image, color: dict, x_global=np.array([1, 0])):
    try:
        height, width, _ = image.shape

        body_color = color["body"]
        point_color = color["point"]

        # Cria uma máscara para filtrar a cor alvo na imagem
        body_mask = cv2.inRange(image, body_color["lower"], body_color["upper"])

        cv2.medianBlur(body_mask, 11, body_mask)
        cv2.imshow('mask', body_mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        body_contours, _ = cv2.findContours(body_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        body_contour = max(body_contours, key=cv2.contourArea)

        body_rect = cv2.minAreaRect(body_contour)
        body_box = cv2.boxPoints(body_rect)
        body_box = np.int32(body_box)

        # Encontra o centro do retângulo
        body_center = body_rect[0]

        cv2.circle(image, (int(body_center[0]), int(body_center[1])), 5, (0, 0, 255), -1)
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        point_mask = cv2.inRange(image, point_color["lower"], point_color["upper"])
        #cv2.medianBlur(point_mask, 11, point_mask)
        cv2.imshow('mask', point_mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        point_countours, _ = cv2.findContours(point_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        point_contour = max(point_countours, key=cv2.contourArea)

        point_rect = cv2.minAreaRect(point_contour)
        point_box = cv2.boxPoints(point_rect)
        point_box = np.int32(point_box)

        # Encontra o centro do retângulo
        point_center = point_rect[0]

        cv2.circle(image, (int(point_center[0]), int(point_center[1])), 5, (255, 0, 0), -1)
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Traçar um vetor do centro do corpo até o centro do ponto
        x = (body_center[0] - point_center[0])
        y =  -(body_center[1] - point_center[1])
        vector = np.array([x, y])
        
        vector = vector / np.linalg.norm(vector)

        angle = math.acos(np.dot(vector, x_global))
        if vector[0] < 0 and vector[1] < 0:
            angle = math.pi + angle
        elif vector[0] < 0 and vector[1] > 0:
            angle = math.pi/2 + angle
        elif vector[0] > 0 and vector[1] < 0:
            angle = 3*math.pi/2 + angle

        return math.degrees(angle)
    except ValueError as e:
        print(e)
        return None

def rotate_image(imagem, angulo=0):
    img = cv2.imread(imagem)
    shape = img.shape
    #img = cv2.resize(img, (shape[1]*5, shape[0]*5))
    image_center = tuple(np.array(img.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angulo, 1.0)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)

    return result

# Imagem de exemplo
image_path = 'src/test/images/file1.jpg'
body_color = (103,207,200)
point_color = (207,42,72)#(121,8,30)
color = color(point_color, body_color, 0.65, 1.35)

# Exemplo de eixos
x_global = {
    "1": np.array([1, 0]),
    "2": np.array([0, 1]),
    "3": np.array([-1, 0]),
    "4": np.array([0, -1])
}
def error():
    erros = []
    for rotation in range(0, 360):
        rotate = rotate_image(image_path, rotation)
        try:
            if rotation == 0 or rotation == 90 or rotation == 180 or rotation == 270 or rotation == 45 or rotation == 135 or rotation == 225 or rotation == 315:
                angle = orient_by_color(rotate, target_color, x_global["1"])
                print(rotation)
                erro = abs(rotation + 90 - angle)
                erros.append(erro)
        except ValueError as e:
            continue
    #print(f'Erro médio: {np.mean(erros)}')
    #print(f'Erro máximo: {np.max(erros)}')
    #print(f'Erro mínimo: {np.min(erros)}')
    #print(f'Desvio padrão: {np.std(erros)}')

#error()
print(orient_by_color(rotate_image(image_path, 0), color, x_global["1"]))

# aumentar saturaçao 4
# mudar metodo rgb 3
# resize e cortar 2
# cortar e resize 1