import cv2
import numpy as np

def rotate_image(imagem, direcao = "norte"):
    if direcao == "norte":
        angulo = 0
    elif direcao == "sul":
        angulo = 180
    elif direcao == "leste":
        angulo = 270
    else:
        angulo = 90
    
    img = cv2.imread(imagem)
    image_center = tuple(np.array(img.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angulo, 1.0)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    cv2.imshow("Rotated Image", result)
    cv2.waitKey(0)
    return result

def detectar_orientacao(imagem, cor, direcao = "norte"):

    img = rotate_image(imagem, direcao)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    lower = cor[0]
    upper = cor[1]

    mask = cv2.inRange(rgb, lower, upper)
    
    # [Altura, Largura]
    norte = mask[0:mask.shape[0]//2, 0:mask.shape[1]]
    sul = mask[mask.shape[0]//2:mask.shape[0], 0:mask.shape[1]]
    leste = mask[0:mask.shape[0], mask.shape[1]//2:mask.shape[1]]
    oeste = mask[0:mask.shape[0], 0:mask.shape[1]//2]

    norte = cv2.countNonZero(norte)
    sul = cv2.countNonZero(sul)
    leste = cv2.countNonZero(leste)
    oeste = cv2.countNonZero(oeste)

    orientacao = max(norte, sul, leste, oeste)

    if orientacao == norte:
        print("Norte") 
    elif orientacao == sul:
        print("Sul")
    elif orientacao == leste:
        print("Leste")
    else:
        print("Oeste")
    

# Testando
imagem = "image.png"
cor = [(123, 32, 32), (180, 50, 50)]
detectar_orientacao(imagem, cor, 'oeste')