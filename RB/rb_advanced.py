import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Load the pre-trained DeepLabv3+ model
model = tf.keras.models.load_model("deeplabv3_plus.h5")

path = input('Enter the path: ')
opath = input('Enter the output path: ')

# Load an image
img = cv2.imread(path)

# Resize the image to match the input size of the network
img = cv2.resize(img, (512, 512))

# Normalize the image
img = (img / 127.5) - 1

# Expand the dimensions to include the batch size
img = np.expand_dims(img, axis=0)

# Predict the segmentation mask
mask = model.predict(img)

# Convert the mask to a binary image
mask = np.argmax(mask, axis=-1)
mask = (mask == 0).astype(np.uint8) * 255

# Use the mask to remove the background
result = cv2.bitwise_and(img[0], img[0], mask=mask)

# Convert back to the original format and save the result
result = (result + 1) * 127.5
result = result.astype(np.uint8)
cv2.imwrite(opath, result)
