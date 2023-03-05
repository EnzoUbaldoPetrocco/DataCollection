import cv2
import numpy as np
import pathlib
from matplotlib import pyplot as plt
import os
import imagehash
from PIL import Image
import sys
sys.path.insert(1, '../')
import Utils.utils

images = []
# Expression of similarity threshold (the more are similar, the higher the value)
# must be: 0 < thresh < 1
thresh = 0.999
distance_comp = 0.75
len_comp = 10

class SimilarImages:

    def delete_all_equal_images(self, image_paths, destination_folder):
        # From image_paths, remove right side of similar images
        # and remove duplicates

        images = []
        for img in image_paths:
            # Duplicates condition
            if img not in images:
                cond = False
                for i in self.similar_images:
                        # check for right side of comparison
                        cond = cond or img == i[1]
                if not cond:
                    images.append(img)

        print(f'Number of images without the similar images: {np.shape(images)}')

        if not os.path.exists(destination_folder):
                print(f'Making directory: {str(destination_folder)}')
                os.makedirs(destination_folder)

        for i, img in enumerate(images):
            image = cv2.imread(str(img))
            cv2.imwrite(destination_folder  + f'/image_{i}.jpeg', image)

    def user_selection(self, image_paths, similar_images, destination_folder):
        print('Here there are the comparings, if you press any key it does nothing: ')
        im_removed = 0
        for k, a in enumerate(similar_images):
            for i,j in a:
                image1 = cv2.imread(str(i))
                image2 = cv2.imread(str(j))
                plt.subplot(1,2,1),plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
                plt.subplot(1,2,1),plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
                choice1 = input('Do you want to keep both? (y/n): ')
                if choice1 == 'y':
                    similar_images.remove([i,j])
                    im_removed = im_removed + 1
                if choice1 == 'n':
                    print(f'Left size: {np.shape(image1)}')
                    print(f'Right size: {np.shape(image2)}')
                    choice2 = input('Do you want to delete left or right? (l/r): ')
                    if choice2 == 'l':
                        # swap the element, the right element is eliminated
                        similar_images[k-im_removed] = [j,i]
        images = []
        for img in image_paths:
            if img not in images:
                cond = False
                for i in similar_images:
                        cond = cond or img == i[1]
                if cond:
                    images.append(img)

        print(f'Number of images without the similar images: {np.shape(images)}')

        if not os.path.exists(destination_folder):
                print(f'Making directory: {str(destination_folder)}')
                os.makedirs(destination_folder)

        for i, img in enumerate(images):
            image = cv2.imread(str(img))
            cv2.imwrite(destination_folder  + f'/image_{i}.jpeg', image)

    def image_feature_extraction(self, image_paths):
        sift = cv2.xfeatures2d.SIFT_create()
        features = []
        for path in image_paths:
            image = cv2.imread(path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            kp, des = sift.detectAndCompute(gray, None)
            features.append(des)

        bf = cv2.BFMatcher()
        similar_images = []
        for i in range(len(features)):
            for j in range(i+1, len(features)):
                matches = bf.knnMatch(features[i], features[j], k=2)
                good_matches = []
                for m, n in matches:
                    if m.distance < self.distance_comp * n.distance:
                        good_matches.append(m)
                if len(good_matches) > self.len_comp:
                    similar_images.append((image_paths[i], image_paths[j]))

        return similar_images

    def image_hashing(self, image_paths):
        images = {}
        for path in image_paths:
            image = Image.open(path)
            hash = str(imagehash.phash(image))
            if hash in images:
                images[hash].append(path)
            else:
                images[hash] = [path]

        return [v for v in images.values() if len(v) > 1]

    def local_and_global_feature_descriptors(self, image_paths):
        # local features
        brisk = cv2.BRISK_create()
        local_features = []
        for path in image_paths:
            image = cv2.imread(str(path))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            kp, des = brisk.detectAndCompute(gray, None)
            local_features.append(des)

        #global features
        sift = cv2.SIFT_create()
        global_features = []
        for path in image_paths:
            image = cv2.imread(str(path))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            kp, des = sift.detectAndCompute(gray, None)
            global_features.append(des)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        similar_images = []
        for i in range(len(global_features)):
            for j in range(i+1, len(global_features)):
                matches = bf.match(local_features[i], local_features[j])
                score = np.dot(global_features[i][0], global_features[j][0].T)
                # Calibration of score
                # Hint: transform the score s.t self.thresh is
                # really the threshold
                score = (score / 100000) - 1.6
                len_matches = len(matches)/100
                local_cond = len_matches > (self.thresh - 0.06) and len_matches < self.thresh
                glob_cond = score > (self.thresh - 0.0005) and score < self.thresh
                if glob_cond and local_cond:
                    image1 = cv2.imread(str(image_paths[i]))
                    image2 = cv2.imread(str(image_paths[j]))
                    plt.subplot(1,2,1),plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
                    plt.subplot(1,2,2),plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
                    plt.show()
                local_cond = len_matches > self.thresh
                glob_cond = score > self.thresh
                if local_cond and glob_cond:
                    similar_images.append((image_paths[i], image_paths[j]))

        return similar_images
    
    
    
    def local_feature_descriptors(self, image_paths):
        brisk = cv2.BRISK_create()
        features = []
        for path in image_paths:
            image = cv2.imread(str(path))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            kp, des = brisk.detectAndCompute(gray, None)
            features.append(des)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        similar_images = []
        for i in range(len(features)):
            for j in range(i+1, len(features)):
                matches = bf.match(features[i], features[j])
                len_matches = len(matches)/100
                print(len_matches)
                if len_matches > (self.thresh - 0.06) and len_matches < self.thresh:
                    image1 = cv2.imread(str(image_paths[i]))
                    image2 = cv2.imread(str(image_paths[j]))
                    plt.subplot(1,2,1),plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
                    plt.subplot(1,2,2),plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
                    plt.show()
                if len_matches > self.thresh:
                    similar_images.append((image_paths[i], image_paths[j]))

        return similar_images

    def global_feature_descriptors(self, image_paths):
        sift = cv2.SIFT_create()
        features = []
        for path in image_paths:
            image = cv2.imread(str(path))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            kp, des = sift.detectAndCompute(gray, None)
            features.append(des)
        similar_images = []
        for i in range(len(features)):
            for j in range(i+1, len(features)):
                score = np.dot(features[i][0], features[j][0].T)
                # Calibration of score
                # Hint: transform the score s.t self.thresh is
                # really the threshold
                score = (score / 100000) - 1.6
                print(score)
                if score > (self.thresh - 0.0005) and score < self.thresh:
                    image1 = cv2.imread(str(image_paths[i]))
                    image2 = cv2.imread(str(image_paths[j]))
                    plt.subplot(1,2,1),plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
                    plt.subplot(1,2,2),plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
                    plt.show()
                if score > self.thresh:
                    similar_images.append((image_paths[i], image_paths[j]))
        print(f'Number of pairs of similar images: {np.shape(similar_images)}')
        return similar_images

    def color_histograms(self, image_paths):
        global images
        features = []
        for path in image_paths:
            image = cv2.imread(str(path))
            hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            features.append(hist.flatten())

        similar_images = []
        for i in range(len(features)):
            for j in range(i+1, len(features)):
                hist1 = features[i]
                hist2 = features[j]
                similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
                if similarity > self.thresh:
                    similar_images.append((image_paths[i], image_paths[j]))
        print(f'Number of pairs of similar images: {np.shape(similar_images)}')
        return similar_images

    def __init__(self, delete_all_images):
        equal_threshold = 0.999
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

        print('Select among these methods for comparing similar images:')
        print('1) color_histograms\n2) global_feature_descriptors\n3) local_feature_descriptors')
        print('4) image_hashing\n5) image_feature_extraction \n6) ' + 
        'local_and_global_feature_descriptors')
        x = input('Enter a number from 1 to 6 in order to decide which method is used (default: color_histograms): ')
        try:
            x = int(x)
        except:
            print('Default: color_histograms')

        print(f'Initial number of the images: {len(image_paths)}')

        if not isinstance(x, str):
            if x == 2:
                if delete_all_images:
                    self.thresh = equal_threshold
                else:
                    self.thresh = float(input('Enter the threshold param: '))
                similar_images = self.global_feature_descriptors(image_paths)
            elif x == 3:
                if delete_all_images:
                    self.thresh = equal_threshold
                else:
                    self.thresh = float(input('Enter the threshold param: '))
                similar_images = self.local_feature_descriptors(image_paths)
            elif x == 4:
                similar_images = self.image_hashing(image_paths)
            elif x == 5:
                self.distance_comp = float(input('Enter the distance_comp param: '))
                self.len_comp = float(input('Enter the length_comp param: '))
                similar_images = self.image_feature_extraction(image_paths)
            elif x == 6:
                if delete_all_images:
                    self.thresh = equal_threshold
                else:
                    self.thresh = float(input('Enter the threshold param: '))
                similar_images = self.local_and_global_feature_descriptors(image_paths)
                
            else:
                if delete_all_images:
                    self.thresh = equal_threshold
                else:
                    self.thresh = float(input('Enter the threshold param: '))
                similar_images = self.color_histograms(image_paths)
        else: 
            if delete_all_images:
                self.thresh = equal_threshold
            else:
                self.thresh = float(input('Enter the threshold param: '))
            similar_images = self.color_histograms(image_paths)

        self.similar_images = similar_images
            
        if delete_all_images:
            self.delete_all_equal_images(image_paths, destination_folder)
            
        