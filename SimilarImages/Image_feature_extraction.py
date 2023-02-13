import cv2
import numpy as np

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
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)
            if len(good_matches) > 10:
                similar_images.append((image_paths[i], image_paths[j]))

    return similar_images

image_paths = [...] # list of image paths
features = extract_features(image_paths)
similar_images = find_similar_images(features, image_paths)
