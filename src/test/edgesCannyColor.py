from orientation_by_color import color
import cv2
import numpy as np

body_color = (103,207,200)
point_color = (207,42,72)#(121,8,30)
cor = color(point_color, body_color, 0.65, 1.35)

image = cv2.imread('src/test/images/file1.jpg')
shape = image.shape
#image = cv2.resize(image, (shape[1]*3, shape[0]*3))
cv2.imshow('Original Image', image)
cv2.waitKey(0)

body_mask = cv2.inRange(image, cor['body']["lower"], cor['body']["upper"])
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
body_mask = cv2.erode(body_mask, kernel, iterations=1)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
body_mask = cv2.dilate(body_mask, kernel, iterations=1)

countours, _ = cv2.findContours(body_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
max_contour = max(countours, key=cv2.contourArea)

bounding_box = cv2.minAreaRect(max_contour)
bounding_box = np.int32(cv2.boxPoints(bounding_box))
cv2.drawContours(image, [bounding_box], -1, (0, 255, 0), 2)


M = cv2.moments(bounding_box)
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])

center_body = (cX, cY)

cv2.circle(image, center_body, 5, (255, 0, 0), -1)





point_mask = cv2.inRange(image, cor['point']["lower"], cor['point']["upper"])
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
point_mask = cv2.erode(point_mask, kernel, iterations=1)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
point_mask = cv2.dilate(point_mask, kernel, iterations=1)

countours, _ = cv2.findContours(point_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
max_contour = max(countours, key=cv2.contourArea)

bounding_box = cv2.minAreaRect(max_contour)
bounding_box = np.int32(cv2.boxPoints(bounding_box))
cv2.drawContours(image, [bounding_box], -1, (0, 255, 0), 2)


M = cv2.moments(bounding_box)
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])

center_point= (cX, cY)

cv2.circle(image, center_body, 5, (255, 0, 0), -1)

cv2.imshow('Body Contour', image)
cv2.waitKey(0)
