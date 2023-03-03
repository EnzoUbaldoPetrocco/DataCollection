import pathlib
import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from math import ceil
import string
from matplotlib.widgets import Slider, Button
import matplotlib.patches as patches
from matplotlib import animation
import os
from copy import deepcopy


class RemoveBackGround:
    # Manual Background Removing
    def slider_update(self,val):
            self.amplitude = int(self.slider.val * 2)

    def draw_discrete_circle_with_boundaries(self,x,y,r, xmax, ymax):
        # Algorithm: 
        # - check which indeces falls in the equation:
        # (x-x0)^2+(y-y0)^2=r^2
        # obv I check only in a rxr matrix then i sum x0 and y0
        indices = []
        temp_indices = []
        x = int(x)
        y = int(y)
        for x_i in range(-r,r+1):
            for y_i in range(-r,r+1): 
                if x_i*x_i+y_i*y_i<=r*r:
                    temp_indices.append([x_i+x,y_i+y])
        for i in temp_indices:
            if i[0]>=0 and i[0]<xmax and i[1]>=0 and i[1]<ymax:
                indices.append([i[0], i[1]])
        return indices
            
    def reset(self, event):
        self.dummy = deepcopy(self.image)
        print('Reset')

    def mouse_click(self, event):
            self.mouse = True

    def mouse_release(self, event):
            self.mouse = False
    
    def updatefig(self, *args):
        x, y = self.x, self.y
        if self.mouse:
            if int(x)>0 and int(x)<=np.shape(self.dummy)[0] and int(y)>0 and int(y)<=np.shape(self.dummy)[1]:
                indices = self.draw_discrete_circle_with_boundaries(x, y,self.amplitude,np.shape(self.dummy)[0],np.shape(self.dummy)[1])
                if not self.invert:
                    for i in indices:     
                        self.dummy[i[1],i[0],:] = [255,255,255]
                else:
                    for i in indices:
                        self.dummy[i[1],i[0]] = self.image[i[1],i[0]]
        self.im.set_data(self.dummy)
        return self.im,

    def mouse_move(self, event):
        if event.xdata!=None and event.ydata!=None and event.xdata>=0 and event.ydata>=0:
            self.x, self.y = event.xdata, event.ydata

    def invert_behavior(self, event):
        self.invert= not self.invert

    def manual_rb(self, image):
        self.mouse = False
        self.invert = False
        mean_slider_value = 5
        self.x, self.y = -mean_slider_value*2,-mean_slider_value*2
        self.amplitude = int(mean_slider_value * 2)
        self.image = image
        self.dummy = deepcopy(self.image)   
        plt.ion()
        self.fig = plt.figure()
        plt.subplots_adjust(bottom=0.35)
        self.im = plt.imshow(self.dummy, animated = True)
        # Slider to control the dimension of the bg remover
        axSlider = plt.axes([0.25, 0.2, 0.65, 0.03])
        self.slider = Slider(axSlider, 'Cursor dimension', 1.0, 10.0, mean_slider_value)
        self.slider.on_changed(self.slider_update)
        # Button to reset the image
        resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
        resbutton = Button(resetax, 'Reset', color='blue',
                hovercolor='red')
        resbutton.on_clicked(self.reset)
        invax = plt.axes([0.1, 0.025, 0.1, 0.04])
        invbutton = Button(invax, 'Invert', color='blue',
                hovercolor='red')
        invbutton.on_clicked(self.invert_behavior)
        ani = animation.FuncAnimation(self.fig, self.updatefig, interval=50, blit=True)          
        # Tie the callbacks with the mouse click
        cid = self.fig.canvas.mpl_connect('button_press_event', self.mouse_click)
        self.fig.canvas.mpl_connect('button_release_event', self.mouse_release)
        plt.connect('motion_notify_event', self.mouse_move)
        return_value = input('Press enter to confirm the choice  ')
        plt.close()
        plt.ioff()
    
    # Background Removing Algorithms
    def add_blank_screen(self, foreground, mask):
        single_thresh = 5
        sum_thresh = 3 * single_thresh
        for i in range(np.shape(foreground)[0]):
            for j in range(np.shape(foreground)[1]):
                # img[i, j] is the RGB pixel at position (i, j)
                # check if it's [0, 0, 0] and replace with [255, 255, 255] if so
                if foreground[i, j].sum() <= sum_thresh and foreground[i,j,0]<single_thresh and foreground[i,j,1]<single_thresh and foreground[i,j,2]<single_thresh:
                    foreground[i, j] = [255, 255, 255]
        return foreground

    def compare(self, s1, s2):
        remove = string.punctuation + string.whitespace
        return s1.translate(str.maketrans(dict.fromkeys(remove))) == s2.translate(str.maketrans(dict.fromkeys(remove)))

    def mog2(self, img):
        # Create a background subtractor object
        fgbg = cv2.createBackgroundSubtractorMOG2()
        # Apply background subtraction to the image
        mask = fgbg.apply(img)
        # Apply morphological operations to improve the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # Multiply the original image with the mask to obtain the foreground
        foreground = img * mask[:, :, np.newaxis]
        return foreground

    def grab_cut(self, img, automated):
        plt.imshow(img),plt.grid(),plt.show()
        assert img is not None, "file could not be read, check with os.path.exists()"
        mask = np.zeros(img.shape[:2],np.uint8)
        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)
        ok = False
        while(not ok):
            if automated:
                x = 1
                y = 1
                w = img.shape[0]
                h = img.shape[1]
            else:
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

            cv2.grabCut(img,mask,rect,bgdModel,fgdModel,10,cv2.GC_INIT_WITH_RECT)
            mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
            # Create a blank background
            background = np.zeros_like(img, dtype=np.uint8)
            foreground = img*mask2[:,:,np.newaxis]
            img_modified = self.add_blank_screen(foreground, img)
            #img_modified = background + foreground
            
            if not automated:
                plt.ion()
                plt.subplot(2,1,1),plt.imshow(img)
                plt.subplot(2,1,2),plt.imshow(img_modified),plt.show()
                dec = input('Is the crop okay? (y/n)')
                plt.ioff()
                if dec == 'y':
                    ok = True
            else:
                ok = True
        return img_modified
    
    def watershed(self, img):
        # Convert the image to grayscale and apply Gaussian blur
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        # Perform Otsu thresholding to obtain a binary image
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Create a marker image using connected component analysis
        _, markers = cv2.connectedComponents(thresh)
        # Apply the Watershed algorithm
        markers = cv2.watershed(img, markers)
        # Create the final mask
        mask = np.where(markers == -1, 0, 1).astype("uint8")
        # Multiply the original image with the mask to obtain the foreground
        foreground = img * mask[:, :, np.newaxis]

        result = self.add_blank_screen(foreground, img)
        # Create a blank background
        #background = np.zeros_like(img, dtype=np.uint8)
        # Combine the foreground and background to get the final result
        #result = foreground + background
        return result

    def k_means_clustering(self, img):
        # Convert the image to a one-dimensional array
        rows, cols, channels = img.shape
        data = img.reshape(rows * cols, channels)
        # Perform K-Means clustering on the image data
        K = 8
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(data.astype(np.float32), K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        # Assign the cluster with the lowest intensity mean value to the background
        background_label = np.argmin(centers[:, 0] + centers[:, 1] + centers[:, 2])
        mask = np.where(labels == background_label, 0, 1).reshape(rows, cols)
        # Multiply the original image with the mask to obtain the foreground
        foreground = img * mask[:, :, np.newaxis]
        result = self.add_blank_screen(foreground, img)
        
        return result
    
    def image_selection(self, modified_images, original_image):
        # Plot the images in order to help the user to decided which image is the best
        #col = 0
        n_row = ceil((len(modified_images) + 1)/2)
        print(len(modified_images))
        #row = 0
        plt.ioff()
        with plt.ion():
            for i, mod_im in enumerate(modified_images):
                print('here')
                ax = plt.subplot(n_row,2,i+1)
                ax.set_title(f'Algorithm {i+1}'), ax.set_xticks([]), ax.set_yticks([])
                plt.imshow(mod_im)
            ax = plt.subplot(n_row, 2, len(modified_images) + 1)
            ax.set_title(f'Original Image')
            ax.set_xticks([]), ax.set_yticks([])
            plt.imshow(original_image)
        choice = int(input('Which image do you want to keep? (press an integer for algorithms or -1 for the original)\n' + 
        'algorithms are applied in the same order as you have chosen before  '))
        plt.close()
        plt.ioff()
        return choice

    def automated_algorithm_selection(self, img_to_save, algorithms, automated, original_image, modified_images):
        for algorithm in algorithms:
            if self.compare(algorithm, '1'):
                modified_images.append(self.mog2(img_to_save))
            elif self.compare(algorithm, '2'):
                modified_images.append(self.k_means_clustering(img_to_save))
            elif self.compare(algorithm, '3'):
                modified_images.append(self.grab_cut(img_to_save, automated))
            else:
                modified_images.append(original_image)
        choice = self.image_selection(modified_images, original_image)
        if choice == -1:
            return original_image
        img_to_save = modified_images[choice-1]
        return img_to_save

    def __init__(self, automated = True):
        n = int(input('Give me the number of paths you want to include: '))
        image_paths = []
        images_to_be_saved = []
        types = ('*.png', '*.jpg', '*.jpeg')
        for i in range(n):
            path = input('Enter the path: ')
            for typ in types:
                image_paths.extend(pathlib.Path(path).glob(typ))
        destination_folder = input('Enter the destination folder: ')

        if not os.path.exists(destination_folder):
                print(f'Making directory: {str(destination_folder)}')
                os.makedirs(destination_folder)

        x = input('Which background removing algorithms do you want to apply?\n' + 
        'Separate the numbers using a comma (,)\n' + 
        '1) mog2 \n2) k_means_clustering \n3) grab_cut\n')

        # Remove spaces
        
        algorithms = x.split(',')
        # For each image I would like to:
        # - decide if you want to apply the algorithms
        # - apply the algorithms
        # - decide if which algorithms generates the desired output
        # - decide if you want to apply another algorithm or continue
        for i, img in enumerate(image_paths):
            original_image = cv2.imread(str(img))
            original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
            img_to_save = original_image
            plt.imshow(original_image),plt.ion(),plt.show()
            print('This is the original image.')
            x = input('Do you want to remove the background? (y/n): ')
            if x == 'y':
                remove_bool = True
            else:
                remove_bool = False
                images_to_be_saved.append(img_to_save)
            while(remove_bool):
                manual_version = input('Do you want to apply background removing manually? ')
                try:
                    manual_version = int(manual_version)
                except:
                    manual_version = 0
                modified_images = []
                if manual_version:
                    self.manual_rb(img_to_save)
                    img_to_save = self.dummy
                else:
                    img_to_save = self.automated_algorithm_selection(img_to_save, 
                                                        algorithms, automated, original_image, modified_images)

                
                x = input('Do you want to apply another algorithm? (y/n) ')
                if x == 'y':
                    remove_bool = True
                else:
                    remove_bool = False
                    images_to_be_saved.append(img_to_save)

        for i, img in enumerate(images_to_be_saved):
            cv2.imwrite(destination_folder + f'/image_{i}.jpeg', img)

