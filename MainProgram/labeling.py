import os
import pathlib
import cv2
from matplotlib import pyplot as plt

class Labeling:
    def __init__(self):
        # Get images paths
        path = input('Enter the path to the images: ')
        dest_path = input('Enter the destination path: ')

        n_classes = int(input('How many classes?'))
        labels = []
        for i in n_classes:
            label = input('Enter label name')
            labels.append(label)

        if not os.path.exists(dest_path):
            print(f'Making directory: {str(dest_path)}')
            os.makedirs(dest_path)

        for label in n_classes:
            if not os.path.exists(dest_path + '/' + label):
                print(f'Making directory: {str(dest_path)}/on{str(label)}')
                os.makedirs(dest_path + '/' + label)

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

        print('In this program the order of labels are numbered, so that' + 
        'you can refer to a label using the position (starting from 0).\n' +
        'At the end of this list of labels I have added the don\'t_know label.')
        # pairs represents a 2D list (map) that is needed to associate an image to a label
        pairs = []
        # Show images
        for img in images:
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)),plt.ion(),plt.show()
            res = input('Select the label, default key will be put in the '+ 
            'don\'t_know folder')
            try: 
                res = int(res)
            except:
                res = len(labels) - 1
            pairs.append([img, res])
            plt.close()

        for i, pair in enumerate(pairs):
            cv2.imwrite(dest_path + f'/{labels[pair[1]]}/' + f'image_{i}', pair[0])

        