import cv2
import numpy as np

path = input('Enter the path: ')
opath = input('Enter the output path: ')

# Load an image
img = cv2.imread(path)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
gray = cv2.GaussianBlur(gray, (3, 3), 0)

# Threshold the image to create a binary mask
_, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY_INV)

# Find contours in the mask
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a black image
mask = np.zeros(img.shape, np.uint8)

# Draw filled white shape on the mask for the largest contour
c = max(contours, key=cv2.contourArea)
cv2.drawContours(mask, [c], 0, (255, 255, 255), -1)

# Bitwise AND of the mask and the original image to remove the background
result = cv2.bitwise_and(img, mask)

# Save the result
cv2.imwrite(opath, result)
