import cv2
import numpy as np

def extract_features(image_paths):
    features = []
    for path in image_paths:
        image = cv2.imread(path)
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        features.append(hist.flatten())

    return features

def find_similar_images(features, image_paths):
    similar_images = []
    for i in range(len(features)):
        for j in range(i+1, len(features)):
            hist1 = features[i]
            hist2 = features[j]
            similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
            if similarity > 0.8:
                similar_images.append((image_paths[i], image_paths[j]))

    return similar_images

image_paths = [...] # list of image paths
features = extract_features(image_paths)
similar_images = find_similar_images(features, image_paths)
