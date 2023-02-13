import numpy as np
import cv2

# Load an image
img = cv2.imread("esempio_remove_background.jpg")

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

# Save the result
cv2.imwrite("k_means_clustering_result.jpg", result)
