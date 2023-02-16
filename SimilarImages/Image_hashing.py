import imagehash
from PIL import Image
import cv2
import numpy as np
import pathlib
from matplotlib import pyplot as plt
import os

images = []

def delete_all_equal_images(image_paths, similar_images, destination_folder):
    images = []
    for img in image_paths:
        if img not in images:
            cond = False
            for i in similar_images:
                    cond = cond or img == i[1]
            if cond:
                images.append(img)

    print(f'Number of images without the similar images: {np.shape(images)}')

    if not os.path.exists(destination_folder):
            print(f'Making directory: {str(destination_folder)}')
            os.makedirs(destination_folder)

    for i, img in enumerate(images):
        image = cv2.imread(str(img))
        cv2.imwrite(destination_folder  + f'/image_{i}.jpeg', image)        
    

def find_similar_images(image_paths):
    images = {}
    for path in image_paths:
        image = Image.open(path)
        hash = str(imagehash.phash(image))
        if hash in images:
            images[hash].append(path)
        else:
            images[hash] = [path]

    return [v for v in images.values() if len(v) > 1]

n = int(input('Give me the number of paths you want to include: '))
image_folder_paths = []
image_paths = []
types = ('*.png', '*.jpg', '*.jpeg')
for i in range(n):
    path = input('Enter the path: ')
    for typ in types:
        image_paths.extend(pathlib.Path(path).glob(typ))
destination_folder = input('Enter the destination folder: ')
similar_images = find_similar_images(image_paths)
delete_all_equal_images(image_paths, similar_images, destination_folder)