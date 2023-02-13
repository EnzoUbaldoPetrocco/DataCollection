import numpy as np
import cv2

# Load an image
img = cv2.imread("esempio_remove_background.jpg")

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

# Save the result
cv2.imwrite("gpt_watershed_result.jpg", result)


