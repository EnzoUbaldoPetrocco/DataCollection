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

def extract_features(image_paths):
    sift = cv2.xfeatures2d.SIFT_create()
    features = []
    for path in image_paths:
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kp, des = sift.detectAndCompute(gray, None)
        features.append(des)

    return features

def find_similar_images(features, image_paths):
    similar_images = []
    for i in range(len(features)):
        for j in range(i+1, len(features)):
            score = np.dot(features[i], features[j].T)
            if score > thresh:
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