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

    # [Altura, Largura]
    norte = mask[0:mask.shape[0]//2, 0:mask.shape[1]]
    sul = mask[mask.shape[0]//2:mask.shape[0], 0:mask.shape[1]]
    leste = mask[0:mask.shape[0], mask.shape[1]//2:mask.shape[1]]
    oeste = mask[0:mask.shape[0], 0:mask.shape[1]//2]
    nordeste = mask[0:mask.shape[0]//2, mask.shape[1]//2:mask.shape[1]]
    sudeste = mask[mask.shape[0]//2:mask.shape[0], mask.shape[1]//2:mask.shape[1]]
    sudoeste = mask[mask.shape[0]//2:mask.shape[0], 0:mask.shape[1]//2]
    noroeste = mask[0:mask.shape[0]//2, 0:mask.shape[1]//2]

    norte = (np.count_nonzero(norte == 255) / norte.size) * 100
    sul = (np.count_nonzero(sul == 255) / sul.size) * 100
    leste = (np.count_nonzero(leste == 255) / leste.size) * 100
    oeste = (np.count_nonzero(oeste == 255) / oeste.size) * 100
    nordeste = (np.count_nonzero(nordeste == 255) / nordeste.size) * 100
    sudeste = (np.count_nonzero(sudeste == 255) / sudeste.size) * 100
    sudoeste = (np.count_nonzero(sudoeste == 255) / sudoeste.size) * 100
    noroeste = (np.count_nonzero(noroeste == 255) / noroeste.size) * 100

    direcoes = {
        "norte": norte,
        "sul": sul,
        "leste": leste,
        "oeste": oeste,
        "nordeste": nordeste,
        "sudeste": sudeste,
        "sudoeste": sudoeste,
        "noroeste": noroeste
    }
    orientacao = max(direcoes, key=direcoes.get)
    print(direcoes)
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
        

        # Desenhar o eixo x local no centro do contorno
        cv2.line(image, (cx, cy), (cx + int(x_axis[0] * 50), cy + int(x_axis[1] * 50)), (0, 255, 0), 2)
        
        # Desenhar o eixo y local no centro do contorno
        cv2.line(image, (cx, cy), (cx + int(y_axis[0] * 50), cy + int(y_axis[1] * 50)), (255, 0, 0), 2)

        # Mostrar a imagem
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(f"O ângulo é: {math.degrees(angle)} graus")
        print(f"A orientação é: {orientacao}")
        if orientacao == "noroeste":
            return math.degrees(angle + math.pi/2)
        elif orientacao == "sul" or orientacao == "sudeste":
            return math.degrees(angle + 3*math.pi/2)
        elif orientacao == "leste" or orientacao == "nordeste":
            return math.degrees(angle)
        elif orientacao == "oeste" or orientacao == "sudoeste":
            return math.degrees(angle + math.pi)        

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
rotation = 0
rotate = rotate_image(image_path, rotation)
rgb = (171, 48, 51)

target_color = rgb

try:
    angle = orient_by_color(rotate, target_color)
    print(f"A orientação é: {angle} graus")
except ValueError as e:
    print(e)