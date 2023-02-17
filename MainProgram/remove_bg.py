import pathlib
import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from math import ceil
class RemoveBackGround:

    def mog2(self, image):
        # Load an image
        img = cv2.imread(image)
        # Create a background subtractor object
        fgbg = cv2.createBackgroundSubtractorMOG2()
        # Apply background subtraction to the image
        mask = fgbg.apply(img)
        # Apply morphological operations to improve the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # Multiply the original image with the mask to obtain the foreground
        foreground = img * mask[:, :, np.newaxis] / 255.0
        # Create a blank background
        background = np.zeros_like(img, dtype=np.uint8)
        # Combine the foreground and background to get the final result
        result = foreground + background
        return result

    def edge_base_segmentation(self, image):
        img = cv2.imread(image)
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply Canny edge detection to the grayscale image
        edges = cv2.Canny(gray, 20, 200)
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

    def watershed(self, image):
        img = cv2.imread(image)
        # Convert the image to grayscale and apply Gaussian blur
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
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
        # Create a blank background
        background = np.zeros_like(img, dtype=np.uint8)
        # Combine the foreground and background to get the final result
        result = foreground + background
        return result

    def grab_cut(self, image, automated):
        img = cv2.imread(image)
        plt.imshow(img),plt.grid(),plt.show()
        assert img is not None, "file could not be read, check with os.path.exists()"
        mask = np.zeros(img.shape[:2],np.uint8)
        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)

        ok = False
        while(not ok):
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
            img_modified = background + foreground
            plt.subplot(2,1,1),plt.imshow(img)
            plt.subplot(2,1,2),plt.imshow(img_modified),plt.show()
            if not automated:
                dec = input('Is the crop okay? (y/n)')
                if dec == 'y':
                    ok = True
            else:
                ok = True
        return img_modified

    def k_means_clustering(self, image):
        img = cv2.imread(image)
        # Convert the image to a one-dimensional array
        rows, cols, channels = img.shape
        data = img.reshape(rows * cols, channels)
        # Perform K-Means clustering on the image data
        K = 4
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(data.astype(np.float32), K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        # Assign the cluster with the lowest intensity mean value to the background
        background_label = np.argmin(centers[:, 0] + centers[:, 1] + centers[:, 2])
        mask = np.where(labels == background_label, 0, 1).reshape(rows, cols)
        # Multiply the original image with the mask to obtain the foreground
        foreground = img * mask[:, :, np.newaxis]
        # Create a blank background
        background = np.zeros_like(img, dtype=np.uint8)
        # Combine the foreground and background to get the final result
        result = foreground + background
        return result


    def __init__(self, automated):
        n = int(input('Give me the number of paths you want to include: '))
        image_paths = []
        images_to_be_saved = []
        types = ('*.png', '*.jpg', '*.jpeg')
        for i in range(n):
            path = input('Enter the path: ')
            for typ in types:
                image_paths.extend(pathlib.Path(path).glob(typ))
        destination_folder = input('Enter the destination folder: ')
        x = input('Which background removing algorithms do you want to apply?\n' + 
        'Separate the numbers using a comma (,)' + 
        '1) mog2\n 2) edge_base_segmentation 3) watershed 4) grab_cut\n' + 
        '5) k_means_clustering')
        algorithms = x.split(',')
        # For each image I would like to:
        # - decide if you want to apply the algorithms
        # - apply the algorithms
        # - decide if which algorithms generates the desired output
        # - decide if you want to apply another algorithm or continue
        for i, img in enumerate(image_paths):
            original_image = cv2.imread(img)
            img_to_save = original_image
            plt.imshow(original_image),plt.ion(),plt.show()
            print('This is the original image.')
            x = input('Do you want to remove the background? (y/n):')
            if x == 'y':
                remove_bool = True
            else:
                remove_bool = False
                images_to_be_saved.append(img_to_save)
            while(remove_bool):
                modified_images = []
                for algorithm in algorithms:
                    if algorithm == '1':
                        modified_images.append(self.mog2(img_to_save))
                    if algorithm == '2':
                        modified_images.append(self.edge_base_segmentation(img_to_save))
                    if algorithm == '3':
                        modified_images.append(self.watershed(img_to_save))
                    if algorithm == '4':
                        modified_images.append(self.grab_cut(img_to_save, automated))
                    if algorithm == '5':
                        modified_images.append(self.k_means_clustering(img_to_save))
                    else:
                        modified_images.append(original_image)

                # Plot the images in order to help the user to decided which image is the best
                col = 0
                n_row = ceil(len(modified_images)/2)
                row = 0
                with plt.ion():
                    for i, mod_im in enumerate(modified_images):
                        col = col + 1
                        if i%n_row==0:
                            row+=1
                            col = 1
                        plt.subplot(row,col,len(modified_images)),plt.imshow(cv2.cvtColor(mod_im, cv2.COLOR_BGR2RGB))
                choice = int(input('Which image do you want to keep? (press an integer)\n Note that the images are filled from rows and the\n' + 
                'algorithms are applied in the same order as you have chosen before'))
                plt.close()
                plt.ioff()
                img_to_save = modified_images[choice-1]
                x = input('Do you want to apply another algorithm? (y/n)')
                if x == 'y':
                    remove_bool = True
                else:
                    remove_bool = False
                    images_to_be_saved.append(img_to_save)

        for i, img in enumerate(images_to_be_saved):
            cv2.imwrite(destination_folder + f'/image_{i}.jpeg', img)
