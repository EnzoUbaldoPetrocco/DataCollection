import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import cv2

plt.rcParams["figure.figsize"] = [10.0, 5.0]
plt.rcParams["figure.autolayout"] = True

def mouse_event(event):
   global x,y
   print('x: {} and y: {}'.format(event.xdata, event.ydata))
   x, y = event.xdata, event.ydata

fig = plt.figure()
cid = fig.canvas.mpl_connect('button_press_event', mouse_event)

ok = False
        # Load the image
img = cv2.imread(str('./esempio_crop_image.jpg'))
plt.imshow(img),plt.grid(),plt.ion(),plt.show()
crop = 1
while(crop):
    while(not ok):
        # Define the coordinates of the region you want to cut
        #x, y, w, h = 50, 60, 200, 300
        ans_1 = input('Proceed? ')
        x1 = x
        y1 = y
        ans_2 = input('Proceed? ')
        x2 = x
        y2 = y

        rect = (x1,y1,x2,y2)
        fig, ax = plt.subplots()
        # Display the image
        ax.imshow(img), plt.grid()
        rect_dr = patches.Rectangle((rect[0], rect[1]), rect[2]-rect[0], rect[3]-rect[1], linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect_dr)
        plt.show()

        like = input('Do you like this cut? (y/n) ')
        plt.close()
        if like == 'y':
            # Crop the image
            cropped_img = img[int(y1):int(y2), int(x1):int(x2)]
            file_name = 'cursor_crop.jpg'
            # Save the cropped image
            cv2.imwrite(file_name, cropped_img)
            ok = True
        else:
            continue
    crop = input('Do you want to crop another image? (0/1, default or 0 = skip) ')
    try:
        n = int(n)
    except:
        print('Default: skip image')
        crop = 0