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


class RemoveBackGround:
    # Manual Background Removing
    def slider_update(self,val):
            self.amplitude = int(self.slider.val * 2)
    def alternative_draw_discrete_circle_with_boundaries(self,x,y,r, xmax, ymax):
        # Algorithm: 
        # - start from (x,y)
        # - go left of r positions.
        # - go up-right until x_i = x
        # - go down right until y_i = y
        # - go down left until x_i = x
        # - go up left until y_i = y
        # - go right of one step, is it x_i=x?
        # - if yes stop, else repeat
        # - At the end, check which indices are out of range
        indices = []
        temp_indices = []
        x = int(x)
        y = int(y)
        temp_indices.append([x,y])
        cond = True
        x_i = x-r
        y_i = y
        print(f'\nx is {x} and y is {y}')
        print(f'r is {r}')
        print(f'x_i is {x_i} and y_i is {y_i}')
        temp_indices.append([x_i, y_i])
        while(cond):
            while(x_i!=x):
                x_i = x_i + 1
                y_i = y_i + 1
                print(f'x_i is {x_i} and y_i is {y_i}')
                temp_indices.append([x_i,y_i])
            while(y_i!=y):
                x_i = x_i + 1
                y_i = y_i - 1
                print(f'x_i is {x_i} and y_i is {y_i}')
                temp_indices.append([x_i,y_i])
            while(x_i!=x):
                x_i = x_i - 1
                y_i = y_i - 1
                print(f'x_i is {x_i} and y_i is {y_i}')
                temp_indices.append([x_i,y_i])
            while(y_i!=y):
                x_i = x_i - 1
                y_i = y_i + 1
                print(f'x_i is {x_i} and y_i is {y_i}')
                temp_indices.append([x_i,y_i])
            x_i = x_i + 1
            print(f'x_i is {x_i} and y_i is {y_i}')
            temp_indices.append([x_i,y_i])
            cond = x_i < x
            print(f'cond is {cond}')
        for i in temp_indices:
            if i[0]>0 and i[0]<xmax and i[1]>0 and i[1]<ymax:
                indices.append([i[0], i[1]])
        print('here')
        return indices
            
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
            if i[0]>0 and i[0]<xmax and i[1]>0 and i[1]<ymax:
                indices.append([i[0], i[1]])
        return indices
            
    def reset(self, event):
        self.dummy = self.image

    def mouse_click(self, event):
            self.mouse = True
    def mouse_release(self, event):
            self.mouse = False
    
    def updatefig(self, *args):
        x, y = self.x, self.y
        if self.mouse:
            if int(x)>0 and int(x)<np.shape(self.dummy)[0] and int(y)>0 and int(y)<np.shape(self.dummy)[1]:
                indices = self.draw_discrete_circle_with_boundaries(x, y,self.amplitude,np.shape(self.dummy)[0],np.shape(self.dummy)[1])
                for i in indices:     
                    self.dummy[i[1],i[0]] = [255,255,255]
        self.im.set_data(self.dummy)
        return self.im,

    def mouse_move(self, event):
        self.x, self.y = event.xdata, event.ydata

    def manual_rb(self, image):
        self.mouse = False
        mean_slider_value = 5
        self.x, self.y = -mean_slider_value*2,-mean_slider_value*2
        self.amplitude = int(mean_slider_value * 2)
        plt.ion()
        self.fig = plt.figure()
        self.image = image
        self.dummy = self.image      
        plt.subplots_adjust(bottom=0.35)
        self.im = plt.imshow(self.dummy, animated = True)
        # Slider to control the dimension of the bg remover
        axSlider = plt.axes([0.25, 0.2, 0.65, 0.03])
        self.slider = Slider(axSlider, 'Cursor dimension', 1.0, 10.0, mean_slider_value)
        self.slider.on_changed(self.slider_update)
        # Button to reset the image
        resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
        button = Button(resetax, 'Reset', color='gold',
                hovercolor='skyblue')
        button.on_clicked(self.reset)
        ani = animation.FuncAnimation(self.fig, self.updatefig, interval=50, blit=True)
        # Initialize the image and the dummy image
          
        # Tie the callback with the mouse click
        cid = self.fig.canvas.mpl_connect('button_press_event', self.mouse_click)
        self.fig.canvas.mpl_connect('button_release_event', self.mouse_release)
        plt.connect('motion_notify_event', self.mouse_move)
        return_value = input('Press enter to confirm the choice')
        plt.close()
        plt.ioff()
    


    # Background Removing Algorithms
    def add_blank_screen(self, foreground, img):
        foreground = 1 -  foreground
        # Create a blank background
        background = np.zeros_like(img, dtype=np.uint8)
        # Combine the foreground and background to get the final result
        result = foreground + background
        result = 1 - result
        return result

    def compare(self, s1, s2):
        remove = string.punctuation + string.whitespace
        return s1.translate(str.maketrans(dict.fromkeys(remove))) == s2.translate(str.maketrans(dict.fromkeys(remove)))

    def mog2(self, img):
        # Create a background subtractor object
        fgbg = cv2.createBackgroundSubtractorMOG2()
        # Apply background subtraction to the image
        mask = fgbg.apply(img)
        # Apply morphological operations to improve the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # Multiply the original image with the mask to obtain the foreground
        foreground = img * mask[:, :, np.newaxis] / 255.0

        result = self.add_blank_screen(foreground, img)
        return result

    def edge_base_segmentation(self, img):
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # Apply Canny edge detection to the grayscale image
        edges = cv2.Canny(gray, 50, 100)
        # Fill the holes in the edges using morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        # Invert the edges to obtain the foreground
        foreground = 255 - edges
        # Create a blank background
        background = np.zeros_like(img, dtype=np.uint8)
        # Combine the foreground and background to get the final result
        result = foreground[:, :, np.newaxis] + background
        return result

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

    def grab_cut(self, img, automated):
        plt.imshow(img),plt.grid(),plt.show()
        assert img is not None, "file could not be read, check with os.path.exists()"
        mask = np.zeros(img.shape[:2],np.uint8)
        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)
        ok = False
        while(not ok):
            if automated:
                x = 0
                y = 0
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
            plt.ion()
            plt.subplot(2,1,1),plt.imshow(img)
            plt.subplot(2,1,2),plt.imshow(img_modified),plt.show()
            if not automated:
                dec = input('Is the crop okay? (y/n)')
                if dec == 'y':
                    ok = True
            else:
                ok = True
            plt.ioff()
        return img_modified

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
        # Create a blank background
        #background = np.zeros_like(img, dtype=np.uint8)
        # Combine the foreground and background to get the final result
        #result = foreground + background
        return result
    
    def image_selection(self, modified_images):
        # Plot the images in order to help the user to decided which image is the best
        #col = 0
        n_row = ceil(len(modified_images)/2)
        #row = 0
        plt.ioff()
        with plt.ion():
            for i, mod_im in enumerate(modified_images):
                #col = col + 1
                #if i%n_row==0:
                #    row+=1
                #    col = 1
                #print(f'Giro {i}. Le variabili sono. \ncol={col}\nn_row={n_row}\nrow{row}\nlunghezza modified images={len(modified_images)}')
                plt.subplot(n_row,2,i+1),plt.imshow(mod_im)
        choice = int(input('Which image do you want to keep? (press an integer)\n Note that the images are filled from rows and the\n' + 
        'algorithms are applied in the same order as you have chosen before'))
        plt.close()
        plt.ioff()
        return choice

    def automated_algorithm_selection(self, img_to_save, algorithm, automated, original_image):
        if self.compare(algorithm, '1'):
            print('1')
            modified_images = self.mog2(img_to_save)
        elif self.compare(algorithm, '2'):
            print('2')
            modified_images =  self.edge_base_segmentation(img_to_save)
        elif self.compare(algorithm, '3'):
            print('3')
            modified_images =  self.watershed(img_to_save)
        elif self.compare(algorithm, '4'):
            print('4')
            modified_images =  self.grab_cut(img_to_save, automated)
        elif self.compare(algorithm, '5'):
            print('5')
            modified_images = self.k_means_clustering(img_to_save)
        else:
            return original_image
        choice = self.image_selection(modified_images)
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
        '1) mog2 \n2) edge_base_segmentation \n3) watershed \n4) grab_cut' + 
        '\n5) k_means_clustering\n')

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
                    for algorithm in algorithms:
                        img_to_save = self.automated_algorithm_selection(img_to_save, 
                                                        algorithm, automated, original_image)

                
                x = input('Do you want to apply another algorithm? (y/n) ')
                if x == 'y':
                    remove_bool = True
                else:
                    remove_bool = False
                    images_to_be_saved.append(img_to_save)

        for i, img in enumerate(images_to_be_saved):
            cv2.imwrite(destination_folder + f'/image_{i}.jpeg', img)

