from improcessing.shape_detection import detect_shapes
import cv2
import os


def process_image(image_path, config_params):
    image = cv2.imread(image_path)
    
    image1, image2 = detect_shapes(image, config_params)

    filename = os.path.basename(image_path)
    
    filename1 = 'shapes_' + filename
    filename2 = 'processed_' + filename

    dir_path = 'static/processed'
    path1 = os.path.join(dir_path, filename1)
    path2 = os.path.join(dir_path, filename2)

    print(path1)
    cv2.imwrite(path1, image1)
    cv2.imwrite(path2, image2)

    print(filename1, filename2)
    return filename1, filename2
