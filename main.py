import cv2
import numpy as np

def rotate_image(imagem, angulo = 0):
    img = cv2.imread(imagem)
    img = cv2.resize(img, (500, 500))
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
    # Remove outliers
    mask = cv2.medianBlur(mask, 7)
    cv2.imshow("mask", mask)
    cv2.waitKey(0)

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

    print(orientacao)

# Testando
imagem = "image.png"
color = (171, 48, 51)

cor = [tuple([0.75*x for x in color]), tuple([1.25*x for x in color])]

detectar_orientacao(imagem, cor, 0)