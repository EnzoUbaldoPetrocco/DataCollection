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
    counter = np.shape(similar_images)[0]
    images = []
    for img in image_paths:
        if img not in images:
            for i in similar_images:
                if img != i[1]:
                    images.append(img)

    print(f'Number of images without the similar images: {np.shape(images)}')

    if not os.path.exists(destination_folder):
            print(f'Making directory: {str(destination_folder)}')
            os.makedirs(destination_folder)

    for i, img in enumerate(images):
        image = cv2.imread(str(img))
        cv2.imwrite(destination_folder  + f'/image_{i}.jpeg', image)

def user_selection(similar_images, destination_folder):
    print('Here there are the comparings, if you press any key it does nothing: ')
    counter = np.shape(similar_images)[0]
    for i,j in similar_images:
        image1 = cv2.imread(str(i))
        image2 = cv2.imread(str(j))
        plt.subplot(1,2,1),plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
        plt.subplot(1,2,1),plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
        print(f'{counter} images left')
        choice1 = input('Do you want to keep both? (y/n): ')
        if choice1 == 'n':
            print(f'Left size: {np.shape(image1)}')
            print(f'Right size: {np.shape(image2)}')
            choice2 = input('Do you want to delete left or right? (l/r): ')
            if choice2 == 'l':
                deleted_image = i
            if choice2 == 'r':
                deleted_image = j
            n_duplicated_elements = similar_images.count(deleted_image)
            for i in range(n_duplicated_elements):
                similar_images.remove(deleted_image)
        counter = counter - 1
    images = []
    for i in similar_images:
        for j in i:
            if j not in images:
                images.append(j)
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