import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

img = cv.imread('utils/images/tiffany-cor-teste.png')
#img = cv.imread('src/test/images/file1.jpg')

img = cv.resize(img, (1000, 1000))

cv.imshow('img', img)
cv.waitKey(0)

canny = cv.Canny(img, 100, 200)
canny = cv.dilate(canny, np.ones((5,5), np.uint8))
cv.imshow('e', canny)
cv.waitKey(0)

# Encontrar contornos
contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Selecionar o maior contorno (baseado na área)
max_contour = max(contours, key=cv.contourArea)

# Desenhar o contorno
#cv.drawContours(img, [max_contour], -1, (0, 255, 0), 2)

# Desenhar o maior contorno no fundo preto
black = np.zeros_like(img)
cv.drawContours(black, [max_contour], -1, (255, 255, 255), 2)

# Mostrar a imagem
cv.imshow('Contour', black)
cv.waitKey(0)