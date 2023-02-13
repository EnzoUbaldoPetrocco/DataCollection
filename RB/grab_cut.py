import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import matplotlib.patches as patches

img = cv.imread('esempio_remove_background.jpg')
plt.imshow(img),plt.grid(),plt.show()
assert img is not None, "file could not be read, check with os.path.exists()"
mask = np.zeros(img.shape[:2],np.uint8)
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

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



cv.grabCut(img,mask,rect,bgdModel,fgdModel,10,cv.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')

# Create a blank background
background = np.zeros_like(img, dtype=np.uint8)
foreground = img*mask2[:,:,np.newaxis]
img_modified = background + foreground
plt.subplot(2,1,1),plt.imshow(img)
plt.subplot(2,1,2),plt.imshow(img_modified),plt.show()

# Save the result
cv.imwrite("grab_cut_result.jpg", img_modified)
