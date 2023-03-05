import cv2
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import pathlib
import os
import numpy as np

count = 0

class Crop:

    def save_image(self, image, file_name, count):
        file_name = file_name.split('.')[0] + f'_{count}.' + file_name.split('.')[1] 
        cv2.imwrite(file_name, image)
        print('Image saved!')


    def mouse_event(self, event):
            print('x: {} and y: {}'.format(event.xdata, event.ydata))
            self.x = event.xdata
            self.y = event.ydata

    def cursor_crop(self, image, file_name):
        global count
        plt.rcParams["figure.figsize"] = [10.0, 6.0]
        plt.rcParams["figure.autolayout"] = True

        fig = plt.figure()
        cid = fig.canvas.mpl_connect('button_press_event', self.mouse_event)

        ok = False
        # Load the image
        img = cv2.imread(str(image))
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)),plt.grid(),plt.ion(),plt.show()
        crop = 1

        choice1 = input('Would you like to crop this image? (0/1)  ')
        try:
            choice1 = int(choice1)
            if choice1!=1:
                crop = 0
                save_ = input('Do you want to save the image?  ')
                try:
                    save_ = int(save_)
                    if save_:
                        count = count + 1
                        # Save the cropped image
                        self.save_image(img, file_name, count)
                except:
                    ...
                
        except:
            crop = 0
            save_ = input('Do you want to save the image?  ')
            try:
                save_ = int(save_)
                if save_:
                    count = count + 1
                    # Save the cropped image
                    self.save_image(img, file_name, count)
            except:
                ...
            
        while(crop):
            while(not ok):
                # Define the coordinates of the region you want to cut
                #x, y, w, h = 50, 60, 200, 300
                ans_1 = input('Click on left up angle and click enter\n')
                x1 = self.x
                y1 = self.y
                ans_2 = input('Click on right bottom angle and click enter\n')
                x2 = self.x
                y2 = self.y

                rect = (x1,y1,x2,y2)
                fig, ax = plt.subplots()
                # Display the image
                ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.grid()
                rect_dr = patches.Rectangle((rect[0], rect[1]), rect[2]-rect[0], rect[3]-rect[1], linewidth=1, edgecolor='r', facecolor='none')
                ax.add_patch(rect_dr)
                plt.show()

                like = input('Do you like this cut? (y/n) ')
                plt.close()
                if like == 'y' or like == '1':
                    # Crop the image
                    cropped_img = img[int(y1):int(y2), int(x1):int(x2)]
                    count = count + 1
                    # Save the cropped image
                    self.save_image(cropped_img, file_name, count)
                    ok = True
                else:
                    continue
            n = input('Do you want to crop another image? (0/1, default or 0 = skip) ')
            try:
                n = int(n)
                if n:
                    ok = False
                else:
                    crop = 0
                    
            except:
                print('Default: skip image')
                crop = 0


    def crop(self, image, file_name):
        global count
        ok = False
        # Load the image
        img = cv2.imread(str(image))
        plt.imshow(img),plt.grid(),plt.ion(),plt.show()
        crop = 1
        choice1 = input('Would you like to crop this image? (0/1)  ')
        try:
            choice1 = int(choice1)
            if choice1!=1:
                crop = 0
                save_ = input('Do you want to save the image?  ')
                try:
                    save_ = int(save_)
                    if save_:
                        count = count + 1
                        # Save the cropped image
                        self.save_image(img, file_name, count)
                except:
                    ...
                
        except:
            crop = 0
            save_ = input('Do you want to save the image?  ')
            try:
                save_ = int(save_)
                if save_:
                    count = count + 1
                    # Save the cropped image
                    self.save_image(img, file_name, count)
            except:
                ...
        
        while(crop):
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
                ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.grid()
                rect_dr = patches.Rectangle((rect[0], rect[1]), rect[2]-rect[0], rect[3]-rect[1], linewidth=1, edgecolor='r', facecolor='none')
                ax.add_patch(rect_dr)
                plt.show()

                like = input('Do you like this cut? (y/n) ')
                plt.close()
                if like == 'y':
                    # Crop the image
                    cropped_img = img[y:y+h, x:x+w]
                    file_name = file_name.split('.')[0] + f'_{count}.' + file_name.split('.')[1] 
                    count = count + 1
                    # Save the cropped image
                    cv2.imwrite(file_name, cropped_img)
                    ok = True
                else:
                    continue
            n = input('Do you want to crop another image? (0/1, default or 0 = skip) ')
            try:
                n = int(n)
                if n:
                    ok = False
                else:
                    crop = 0
            except:
                print('Default: skip image')
                crop = 0
            
    def __init__(self, cursor_mode):
        global count
        n = int(input('Give me the number of paths you want to include: '))
        image_paths = []
        types = ('*.png', '*.jpg', '*.jpeg')
        for i in range(n):
            path = input('Enter the path: ')
            for typ in types:
                image_paths.extend(sorted(pathlib.Path(path).glob(typ)))
        destination_folder = input('Enter the destination folder: ')

        if not os.path.exists(destination_folder):
                print(f'Making directory: {str(destination_folder)}')
                os.makedirs(destination_folder)

        
        count = 0
        for i, im in enumerate(image_paths):
            print(f'Image number {i}')
            if cursor_mode:
                self.cursor_crop(im, destination_folder +  f'/image.jpeg')
            else:
                self.crop(im, destination_folder + f'/image.jpeg')
            plt.close()
