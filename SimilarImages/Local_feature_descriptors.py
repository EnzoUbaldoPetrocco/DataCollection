import cv2
import numpy as np
import pathlib
from matplotlib import pyplot as plt
import os

images = []

thresh = 10

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
    brisk = cv2.BRISK_create()
    features = []
    for path in image_paths:
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kp, des = brisk.detectAndCompute(gray, None)
        features.append(des)

    return features

def find_similar_images(features, image_paths):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    similar_images = []
    for i in range(len(features)):
        for j in range(i+1, len(features)):
            matches = bf.match(features[i], features[j])
            if len(matches) > thresh:
                similar_images.append((image_paths[i], image_paths[j]))

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
