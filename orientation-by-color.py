import cv2
import numpy as np
import math

def orient_by_color(image, target_color):
    # Converter a imagem de BGR para RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Definir os limites inferior e superior para a cor alvo em RGB
    lower_color = np.array([target_color[0] - 10, target_color[1] - 10, target_color[2] - 10], dtype=np.uint8)
    upper_color = np.array([target_color[0] + 10, target_color[1] + 10, target_color[2] + 10], dtype=np.uint8)
    
    # Tamanho da imagem
    height, width, _ = rgb_image.shape
    # Criar uma máscara para filtrar a cor alvo na imagem
    mask = cv2.inRange(rgb_image, lower_color, upper_color)

    # Remover outliers
    mask = cv2.medianBlur(mask, 7)

    # Encontrar os contornos dos objetos na máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # Encontrar o maior contorno
        contour = max(contours, key=cv2.contourArea)
        
        # Calcular o centro do contorno
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = 0, 0
        # Determinar o quadrante
        center_x = width // 2
        center_y = height // 2
        if cx > center_x and cy <= center_y:
            quadrante = 1
        elif cx <= center_x and cy < center_y:
            quadrante = 2
        elif cx < center_x and cy >= center_y:
            quadrante = 3   
        elif cx >= center_x and cy > center_y:
            quadrante = 4
    
        # Encontrar o retângulo que envolve o contorno
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int32(box)
        
        # Calcular o vetor que representa o eixo x local (parte mais longa)
        if rect[1][0] > rect[1][1]:
            x_axis = np.array([box[1][0] - box[0][0], box[1][1] - box[0][1]])
            y_axis = np.array([box[2][0] - box[1][0], box[2][1] - box[1][1]])
        else:
            x_axis = np.array([box[2][0] - box[1][0], box[2][1] - box[1][1]])
            y_axis = np.array([box[1][0] - box[0][0], box[1][1] - box[0][1]])
        
        # Normalizar os vetores
        x_axis = x_axis / np.linalg.norm(x_axis)
        y_axis = y_axis / np.linalg.norm(y_axis)

        # Inverter o sentido do vetor y_axis
        y_axis = -y_axis

        # Calcular o vetor que representa o eixo x global
        x_global = np.array([1, 0])

        # Calcular o ângulo entre o vetor do eixo x local e o vetor do eixo x global utilizando produto escalar
        angle = np.arccos(np.dot(x_axis, x_global))
        
        if quadrante == 1:
            return math.degrees(angle)
        elif quadrante == 2:
            return math.degrees(math.pi - angle)
        elif quadrante == 3:
            return math.degrees(math.pi + angle)
        elif quadrante == 4:
            return math.degrees(2*math.pi - angle)

    else:
        raise ValueError("Nenhum contorno encontrado.")

def rotate_image(imagem, angulo=0):
    img = cv2.imread(imagem)
    
    image_center = tuple(np.array(img.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angulo, 1.0)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)

    return result

# Exemplo de uso
image_path = 'image.png'
rgb = (171, 48, 51)

target_color = rgb


erros = []
for rotation in range(0, 180):
    rotate = rotate_image(image_path, rotation)
    try:
        angle = orient_by_color(rotate, target_color)
        erro = abs(rotation + 90 - angle)
        erros.append(erro)
    except ValueError as e:
        continue


print(f'Erro médio: {np.mean(erros)}')
print(f'Erro máximo: {np.max(erros)}')
print(f'Erro mínimo: {np.min(erros)}')
print(f'Desvio padrão: {np.std(erros)}')