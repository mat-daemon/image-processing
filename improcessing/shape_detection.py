import matplotlib.pyplot as plt
from skimage import io, color, exposure, transform
import numpy as np
import cv2
import matplotlib.pyplot as plt
from improcessing.sobel import sobel


def approx_with_circle(image, contour):
    (x,y),radius = cv2.minEnclosingCircle(contour) 
    center = (int(x),int(y))
    radius = int(radius)
    cv2.circle(image,center,radius,(255,255,0),10)
    cv2.putText(image, "Circle", (center[0]-35, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 3)


def approx_with_rectangle(image, approx):
    x, y, w, h = cv2.boundingRect(approx)
    aspect_ratio = float(w) / h

    if 0.5 <= aspect_ratio <= 1.5:
        shape_name = "Square"
    else:
        shape_name = "Rectangle"
    cv2.drawContours(image, [approx], 0, (255, 255, 0), 10)
    cv2.putText(image, shape_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 3)


def approx_with_triangle(image, approx):
    M = cv2.moments(approx)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        cv2.drawContours(image, [approx], 0, (255, 255, 0), 10)
        cv2.putText(image, "Triangle", (cx - 40, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)


def detect_shape(image, contour):
    approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
    area = cv2.contourArea(contour)

    min_area = 100

    if area > min_area:
        if len(approx) == 3:
            approx_with_triangle(image, approx)
        elif len(approx) == 4:
            approx_with_rectangle(image, approx)
        elif len(approx) > 5:
            approx_with_circle(image, contour)
        else:
            shape_name = "Polygon"


def detect_shapes(image, config_params):
    image_gray = (color.rgb2gray(image) * 255).astype(np.uint8)

    if config_params["GaussianBlur"]:
        image_gray = cv2.GaussianBlur(image, (5, 5), 0) 

    if config_params["Sobel"]:
        _, _, grad_magnitude = sobel(image_gray)
    else:
        grad_magnitude = cv2.Canny(image_gray, threshold1=100, threshold2=200)

    _, grad_magnitude = cv2.threshold(grad_magnitude, 70, 255, cv2.THRESH_BINARY)

    if config_params["DilateAndError"]:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        grad_magnitude = cv2.dilate(grad_magnitude, kernel, iterations=1)
        grad_magnitude = cv2.erode(grad_magnitude, kernel, iterations=1)

    contours, _ = cv2.findContours(grad_magnitude, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    min_area = 100
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            detect_shape(image, contour)

    return image, grad_magnitude
