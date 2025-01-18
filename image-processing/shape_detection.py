import matplotlib.pyplot as plt
from skimage import io, color, exposure, transform
import numpy as np
import cv2
import matplotlib.pyplot as plt

from sobel import sobel



image = cv2.imread('images/chessboard.webp')

image_gray = (color.rgb2gray(image) * 255).astype(np.uint8)

# image = cv2.GaussianBlur(image, (5, 5), 0) 

# image_grad_x, image_grad_y, grad_magnitude = sobel(image_gray)
grad_magnitude = cv2.Canny(image_gray, threshold1=100, threshold2=200)

_, grad_magnitude = cv2.threshold(grad_magnitude, 70, 255, cv2.THRESH_BINARY)

# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# grad_magnitude = cv2.dilate(grad_magnitude, kernel, iterations=1)
# grad_magnitude = cv2.erode(grad_magnitude, kernel, iterations=1)

contours, _ = cv2.findContours(grad_magnitude, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


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
    cv2.drawContours(grad_magnitude, [approx], 0, (255, 255, 0), 10)
    cv2.putText(grad_magnitude, shape_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 3)


def detect_shapes(image, contour):
    approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
    area = cv2.contourArea(contour)

    min_area = 100

    if area > min_area:
        if len(approx) == 3:
            shape_name = "Triangle"
            cv2.drawContours(grad_magnitude, [approx], 0, (255, 255, 0), 10)
            cv2.putText(grad_magnitude, shape_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 3)
        elif len(approx) == 4:
            approx_with_rectangle(grad_magnitude, approx)
        elif len(approx) > 5:
            approx_with_circle(grad_magnitude, contour)
        else:
            shape_name = "Polygon"


min_area = 100
for contour in contours:
    area = cv2.contourArea(contour)
    if area > min_area:
        detect_shapes(image, contour)

plt.figure(figsize=(10, 5))
# plt.imshow(image, cmap='gray')
plt.imshow(grad_magnitude, cmap='gray')
plt.show()
