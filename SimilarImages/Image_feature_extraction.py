import cv2
import numpy as np
import pathlib
from matplotlib import pyplot as plt
import os

images = []


distance_comp = 0.75
len_comp = 10

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
    bf = cv2.BFMatcher()
    similar_images = []
    for i in range(len(features)):
        for j in range(i+1, len(features)):
            matches = bf.knnMatch(features[i], features[j], k=2)
            good_matches = []
            for m, n in matches:
                if m.distance < distance_comp * n.distance:
                    good_matches.append(m)
            if len(good_matches) > len_comp:
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