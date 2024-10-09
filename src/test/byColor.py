import cv2
import json
from functions.color import color
from functions.points import points
from functions.angle import angle

with open('src/test/eixos.json', 'r') as file:
    eixos = json.load(file)

x_global = eixos['x_global']

body_color = (81, 166, 142)#(96, 191, 164)
point_color = (217, 43, 75)

cor = color(point_color, body_color, 50)

image = cv2.imread('src/test/images/box/file1.jpg')
shape = image.shape
prop = 500/shape[1]
new_shape = (int(shape[1]*prop), int(shape[0]*prop))
image = cv2.resize(image, new_shape)

centers = points(image, cor, False)

angle = angle(*centers, x_global['1'])

print(int(angle))