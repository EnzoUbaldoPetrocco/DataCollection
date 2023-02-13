import numpy as np
import cv2

# Load an image
img = cv2.imread("esempio_remove_background.jpg")

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

# Save the result
cv2.imwrite("edge_base_segmentation_result.jpg", result)
