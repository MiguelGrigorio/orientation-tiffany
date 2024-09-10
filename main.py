import cv2
import numpy as np

def rotate_image(imagem, direcao = "norte"):
    if direcao == "norte":
        angulo = 25
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

    return result

def detectar_orientacao(imagem, cor, direcao = "norte"):

    img = rotate_image(imagem, direcao)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    lower = cor[0]
    upper = cor[1]

    mask = cv2.inRange(rgb, lower, upper)
    #mask = cv2.bitwise_not(mask)
    # Remove outliers
    mask = cv2.medianBlur(mask, 5)
    cv2.imshow("Mask", mask)
    cv2.waitKey(0)
    # [Altura, Largura]
    norte = mask[0:mask.shape[0]//2, 0:mask.shape[1]]
    sul = mask[mask.shape[0]//2:mask.shape[0], 0:mask.shape[1]]
    leste = mask[0:mask.shape[0], mask.shape[1]//2:mask.shape[1]]
    oeste = mask[0:mask.shape[0], 0:mask.shape[1]//2]

    total = cv2.countNonZero(mask)
    norte = cv2.countNonZero(norte) / total
    sul = cv2.countNonZero(sul) / total
    leste = cv2.countNonZero(leste) / total
    oeste = cv2.countNonZero(oeste) / total
    nordeste = (norte + leste) / 2*total
    sudeste = (sul + leste) / 2*total
    sudoeste = (sul + oeste) / 2*total
    noroeste = (norte + oeste) / 2*total

    orientacao = max(norte, sul, leste, oeste, nordeste, sudeste, sudoeste, noroeste)

    if orientacao == norte:
        print("Norte") 
    elif orientacao == sul:
        print("Sul")
    elif orientacao == leste:
        print("Leste")
    elif orientacao == oeste:
        print("Oeste")
    elif orientacao == nordeste:
        print("Nordeste")
    elif orientacao == sudeste:
        print("Sudeste")
    elif orientacao == sudoeste:
        print("Sudoeste")
    else:
        print("Noroeste")

# Testando
imagem = "image.png"
color = (171, 48, 51)

cor = [tuple([0.75*x for x in color]), tuple([1.25*x for x in color])]

detectar_orientacao(imagem, cor)