import cv2
import numpy as np

def edges_canny(image, dilate: bool = False):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (9, 9), 0)

    cv2.imshow('Blurred Image', image)
    cv2.waitKey(0)

    edges = cv2.Canny(image, 100, 200)
    if dilate:
        kernel = np.ones((4, 4), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
    return edges


image = cv2.imread('src/test/images/file.jpg')
shape = image.shape
image = cv2.resize(image, (shape[1]*3, shape[0]*3))
cv2.imshow('Original Image', image)
cv2.waitKey(0)

edges = edges_canny(image, dilate = False)
cv2.imshow('Edges Image', edges)
cv2.waitKey(0)

contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


max_contour_closed = max(contours, key=cv2.isContourConvex)
max_contour_area = max(contours, key=cv2.contourArea)

black = np.zeros_like(image)
cv2.drawContours(black, [max_contour_closed], -1, (0, 255, 0), 2) # Green
cv2.drawContours(black, [max_contour_area], -1, (255, 0, 0), 2) # Blue

cv2.imshow('Contour Image', black)
cv2.waitKey(0)
