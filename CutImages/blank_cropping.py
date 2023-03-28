import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import cv2

def blank_crop(img):
    # iterate by row to have first y
    thresh = 250
    r,c,d = np.shape(img)
    cond = False
    for i in range(r):
        for j in range(c):
            for k in range(d):
                if img[i,j,k]<=thresh:
                    if not cond:
                        print(f'Point is {i},{j}')
                        y1 = i
                    cond = True
    # iterate by columns to have first x
    cond = False
    for i in range(c):
        for j in range(r):
            for k in range(d):
                if img[j,i,k]<=thresh:
                    if not cond:
                        print(f'Point is {i},{j}')
                        x1 = i
                    cond = True
    # iterate by inverted rows to have last y
    cond = False
    for i in range(r):
        for j in range(c):
            for k in range(d):
                if img[r-i-1,c-j-1,k]<=thresh:
                    if not cond:
                        print(f'Point is {r-i-1},{c-j-1}')
                        y2 = r-i-1
                    cond = True
    # iterate by inverted columns to have last x
    cond = False
    for i in range(c):
        for j in range(r):
            for k in range(d):
                if img[r-j-1,c-i-1,k]<=thresh:
                    if not cond:
                        print(f'Point is {r-j-1},{c-i-1}')
                        x2 = c-i-1
                    cond = True
    return [x1, y1, x2, y2]

    

plt.rcParams["figure.figsize"] = [10.0, 5.0]
plt.rcParams["figure.autolayout"] = True

fig = plt.figure()

ok = False
        # Load the image
img = cv2.imread(str('./image_705.jpg'))
plt.imshow(img),plt.grid(),plt.ion(),plt.show()

x1,y1,x2,y2 = blank_crop(img)

rect = (x1,y1,x2,y2)
fig, ax = plt.subplots()
# Display the image
ax.imshow(img), plt.grid()
rect_dr = patches.Rectangle((rect[0], rect[1]), rect[2]-rect[0], rect[3]-rect[1], linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect_dr)
plt.show()

like = input('Do you like this cut? (y/n) ')
plt.close()
       