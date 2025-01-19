import numpy as np


def sobel(image):
    kernel_x = np.array([[1, 0, -1],
                         [2, 0, -2],
                         [1, 0, -1]])

    kernel_y = kernel_x.transpose()
    
    image_height, image_width = image.shape
    kernel_height, kernel_width = kernel_x.shape

    pad_h = kernel_height // 2
    pad_w = kernel_width // 2

    padded_image = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)

    image_grad_x = np.zeros_like(image, dtype=np.float64)
    image_grad_y = np.zeros_like(image, dtype=np.float64)

    for i in range(image_height):
        for j in range(image_width):
            covered_image = padded_image[i:i+kernel_height, j:j+kernel_width]
            image_grad_x[i][j] = np.sum(kernel_x*covered_image)
            image_grad_y[i][j] = np.sum(kernel_y*covered_image)

    grad_magnitude = np.sqrt(image_grad_x ** 2 + image_grad_y ** 2)
    grad_magnitude = ((grad_magnitude / np.max(grad_magnitude)) * 255).astype(np.uint8)

    return image_grad_x, image_grad_y, grad_magnitude