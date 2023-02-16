import pathlib
import cv2
from matplotlib import pyplot as plt
import os
import numpy as np

# Get images paths
path = input('Enter the path to the images: ')
dest_path = input('Enter the destination path: ')



# Making destination directories
if not os.path.exists(dest_path):
            print(f'Making directory: {str(dest_path)}')
            os.makedirs(dest_path)
if not os.path.exists(dest_path + '/on'):
            print(f'Making directory: {str(dest_path)}/on')
            os.makedirs(dest_path + '/on')
if not os.path.exists(dest_path + '/off'):
            print(f'Making directory: {str(dest_path)}/off')
            os.makedirs(dest_path + '/off')
if not os.path.exists(dest_path + '/dont_know'):
            print(f'Making directory: {str(dest_path)}/dont_know')
            os.makedirs(dest_path + '/dont_know')

types = ('*.png', '*.jpg', '*.jpeg')
image_paths = []
images = []
for typ in types:
    image_paths.extend(pathlib.Path(path).glob(typ))

for pat in image_paths:
    images.append(cv2.imread(str(pat)))

on_images = []
off_images = []
doubt_images = []

# Show images
for img in images:
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)),plt.ion(),plt.show()
    res = input('Is this item on/off/don\'t know? (o/f/d): ')
    if res == 'o':
        on_images.append(img)
    elif res == 'f':
        off_images.append(img)
    else:
        doubt_images.append(img)
    plt.close()

for i, img in enumerate(on_images):
    cv2.imwrite(dest_path + '/on/' + f'image_{i}', img)
for i, img in enumerate(off_images):
    cv2.imwrite(dest_path + '/off/' + f'image_{i}', img)
for i, img in enumerate(doubt_images):
    cv2.imwrite(dest_path + '/dont_know/' + f'image_{i}', img)