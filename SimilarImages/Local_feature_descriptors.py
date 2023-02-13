import cv2
import numpy as np

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
            if len(matches) > 10:
                similar_images.append((image_paths[i], image_paths[j]))

    return similar_images

image_paths = [...] # list of image paths
features = extract_features(image_paths)
similar_images = find_similar_images(features, image_paths)
