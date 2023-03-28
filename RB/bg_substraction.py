import numpy as np
import cv2

# Load an image
img = cv2.imread("esempio_remove_background.jpg")
#img = img * 255.0
# Create a background subtractor object
fgbg = cv2.createBackgroundSubtractorMOG2()

# Apply background subtraction to the image
mask = fgbg.apply(img)
# Apply morphological operations to improve the mask
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# Multiply the original image with the mask to obtain the foreground
foreground = img * mask[:, :, np.newaxis] #/ 255.0

# Create a blank background
background = np.zeros_like(img, dtype=np.uint8)

# Combine the foreground and background to get the final result
result = foreground + background


   

# Save the result
cv2.imwrite("bg_background_result.jpg", foreground)


