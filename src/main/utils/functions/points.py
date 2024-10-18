import cv2
import numpy as np

def points(image: np.ndarray, cor: dict, show: bool = False):
    if show:
        cv2.imshow('Original', image)
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

    circle = cv2.minEnclosingCircle(max_contour)

    center_point = circle[0]
    center_point = (int(center_point[0]), int(center_point[1]))

    cv2.circle(image, center_point, int(circle[1]), (0, 255, 0), 2)


    cv2.circle(image, center_body, 5, (255, 0, 0), -1)
    cv2.circle(image, center_point, 5, (0, 0, 0), -1)

    if show:
        cv2.imshow('Body Contour', image)
        cv2.waitKey(0)
    return center_body, center_point
