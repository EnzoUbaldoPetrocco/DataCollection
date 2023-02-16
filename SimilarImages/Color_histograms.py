import cv2
import numpy as np
import pathlib
from matplotlib import pyplot as plt
import os

images = []
# Expression of similarity threshold (the more are similar, the higher the value)
# must be: 0 < thresh < 1
thresh = 0.99999

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
    
def extract_features(image_paths):
    global images
    features = []
    for path in image_paths:
        image = cv2.imread(str(path))
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        features.append(hist.flatten())
    return features

def find_similar_images(features, image_paths):
    global images
    similar_images = []
    for i in range(len(features)):
        for j in range(i+1, len(features)):
            hist1 = features[i]
            hist2 = features[j]
            similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
            if similarity > thresh:
                similar_images.append((image_paths[i], image_paths[j]))
    print(f'Number of pairs of similar images: {np.shape(similar_images)}')
    return similar_images

n = int(input('Give me the number of paths you want to include: '))
image_folder_paths = []
image_paths = []
types = ('*.png', '*.jpg', '*.jpeg')
for i in range(n):
    path = input('Enter the path: ')
    for typ in types:
        image_paths.extend(pathlib.Path(path).glob(typ))
destination_folder = input('Enter the destination folder: ')
features = extract_features(image_paths)
similar_images = find_similar_images(features, image_paths)
delete_all_equal_images(image_paths, similar_images, destination_folder)