import cv2
from matplotlib import pyplot as plt

# Load the image
img = cv2.imread("esempio_crop_image.jpg")
plt.imshow(img),plt.grid(),plt.ion(),plt.show()

# Define the coordinates of the region you want to cut
#x, y, w, h = 50, 60, 200, 300
x = int(input('Enter the x of the anchor point of the rectangle: '))
y = int(input('Enter the y of the anchor point of the rectangle: '))
w = int(input('Enter the width of the rectangle: '))
h = int(input('Enter the height of the rectangle: '))
# Crop the image
cropped_img = img[y:y+h, x:x+w]

# Save the cropped image
cv2.imwrite("cropped_image.jpg", cropped_img)
