import cv2
import numpy as np
import math

def orient_by_color(image, target_color, x_global=np.array([1, 0])):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Define um intervalo para detectar a cor alvo (verificar iluminação local)
    lower_color = np.array([target_color[0]*0.75, target_color[1]*0.75, target_color[2]*0.75], dtype=np.uint8)
    upper_color = np.array([target_color[0]*1.25, target_color[1]*1.25, target_color[2]*1.25], dtype=np.uint8)
    
    height, width, _ = rgb_image.shape

    # Cria uma máscara para filtrar a cor alvo na imagem
    mask = cv2.inRange(rgb_image, lower_color, upper_color)

    # Remove outliers
    mask = cv2.medianBlur(mask, 7)

    # Encontra os contornos dos objetos na máscara (fita)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        contour = max(contours, key=cv2.contourArea)
        
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = 0, 0
        
        # Determina o quadrante para ajustar o ângulo
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
    
        # Encontra o retângulo que envolve o contorno
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int32(box)
        
        # Calcula o vetor do contorno
        if rect[1][0] > rect[1][1]:
            axis = np.array([box[1][0] - box[0][0], box[1][1] - box[0][1]])
        else:
            axis = np.array([box[2][0] - box[1][0], box[2][1] - box[1][1]])

        # Normaliza os vetores
        axis = axis / np.linalg.norm(axis)

        # Calcula o ângulo entre o vetor do contorno e o eixo x global
        angle = np.arccos(np.dot(axis, x_global))
        
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

# Imagem de exemplo
image_path = 'utils/images/tiffany-cor-teste.png'
target_color = (171, 48, 51)

# Exemplo de eixos
x_global = {
    "1": np.array([1, 0]),
    "2": np.array([0, 1]),
    "3": np.array([-1, 0]),
    "4": np.array([0, -1])
}
erros = []
for rotation in range(0, 180):
    rotate = rotate_image(image_path, rotation)
    try:
        angle = orient_by_color(rotate, target_color, x_global["1"])
        erro = abs(rotation + 90 - angle)
        erros.append(erro)
    except ValueError as e:
        continue

print(f'Erro médio: {np.mean(erros)}')
print(f'Erro máximo: {np.max(erros)}')
print(f'Erro mínimo: {np.min(erros)}')
print(f'Desvio padrão: {np.std(erros)}')