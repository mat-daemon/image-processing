from improcessing.shape_detection import detect_shapes
import cv2
import os
from datetime import datetime


def process_image(image_path, config_params):
    image = cv2.imread(image_path)
    
    image1, image2 = detect_shapes(image, config_params)

    filename = os.path.basename(image_path)
    
    timestamp = datetime.now().strftime('%y%m%d%H%M%S')

    filename1 = 'shapes_' + timestamp + "_" + filename
    filename2 = 'processed_' + timestamp + "_" + filename

    dir_path = 'static/processed'
    path1 = os.path.join(dir_path, filename1)
    path2 = os.path.join(dir_path, filename2)

    cv2.imwrite(path1, image1)
    cv2.imwrite(path2, image2)

    return filename1, filename2
