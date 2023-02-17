import cv2
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import pathlib

class Crop:
    def crop(self, image, file_name):
        ok = False
        # Load the image
        img = cv2.imread(image)
        plt.imshow(img),plt.grid(),plt.ion(),plt.show()
        n = input('How many objects do you see? (default or 0 = skip)')
        try:
            n = int(n)
        except:
            print('Default: skip image')
        if not isinstance(n, str):
            if n > 0:
                for i in range(n):
                    while(not ok):
                        # Define the coordinates of the region you want to cut
                        #x, y, w, h = 50, 60, 200, 300
                        x = int(input('Enter the x of the anchor point of the rectangle: '))
                        y = int(input('Enter the y of the anchor point of the rectangle: '))
                        w = int(input('Enter the width of the rectangle: '))
                        h = int(input('Enter the height of the rectangle: '))

                        rect = (x,y,w+x,h+y)
                        fig, ax = plt.subplots()
                        # Display the image
                        ax.imshow(img)
                        rect_dr = patches.Rectangle((rect[0], rect[1]), rect[2]-rect[0], rect[3]-rect[0], linewidth=1, edgecolor='r', facecolor='none')
                        ax.add_patch(rect_dr)
                        plt.show()

                        like = input('Do you like this cut? (y/n)')
                        if like == 'y':
                            # Crop the image
                            cropped_img = img[y:y+h, x:x+w]
                            file_name = file_name.split('.')[0] + f'_{i}.' + file_name.split('.')[1] 
                            # Save the cropped image
                            cv2.imwrite(file_name, cropped_img)
                            ok = True
                        else:
                            continue
            
    def __init__(self):
        n = int(input('Give me the number of paths you want to include: '))
        image_paths = []
        types = ('*.png', '*.jpg', '*.jpeg')
        for i in range(n):
            path = input('Enter the path: ')
            for typ in types:
                image_paths.extend(pathlib.Path(path).glob(typ))
        destination_folder = input('Enter the destination folder: ')

        for im in image_paths:
            self.crop(im, destination_folder + f'/image.jpeg')
