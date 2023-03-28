import os
import pathlib
import cv2
from matplotlib import pyplot as plt
import sys
sys.path.insert(1, '../')
import Utils.utils

class Labeling:
    def __init__(self):
        plt.rcParams['figure.dpi'] = 125
        # Get images paths
        path = input('Enter the path to the images: ')
        dest_path = input('Enter the destination path: ')

        n_classes = int(input('How many classes? '))
        labels = ['dontknow']
        for i in range(n_classes):
            label = input('Enter label name ')
            labels.append(label)

        if not os.path.exists(dest_path):
            print(f'Making directory: {str(dest_path)}')
            os.makedirs(dest_path)

        for label in labels:
            if not os.path.exists(dest_path + '/' + label):
                print(f'Making directory: {str(dest_path)}/{str(label)}')
                os.makedirs(dest_path + '/' + label)


        types = ('*.png', '*.jpg', '*.jpeg')
        image_paths = []
        images = []
        for typ in types:
            image_paths.extend(sorted(pathlib.Path(path).glob(typ)))

        for pat in image_paths:
            images.append(cv2.imread(str(pat)))
        # Shift to insert anytime the program is interrupted
        shift = 0
        images = images[shift:len(images) - 1]
        print('In this program the order of labels are numbered, so that' + 
        'you can refer to a label using the position (starting from 0).\n' +
        'At the end of this list of labels I have added the don\'t_know label. ')
        # Show images
        for j, img in enumerate(images):
            print(f'{j+1}/{len(images)}')
            print(f'Image {image_paths[shift + j+1]}')
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)),plt.ion(),plt.show()
            res = Utils.utils.options(labels)
            plt.close('all')
            destination = dest_path + f'/{labels[res-1]}/' + f'image_{shift + j}.jpg'
            cv2.imwrite(destination, img)
            print(f'Image saved in {destination}')

            

        