import numpy as np
import tensorflow as tf
import keras
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
import pathlib
from tensorflow.keras.utils import img_to_array

gpus = tf.config.experimental.list_physical_devices('GPU')
for device in gpus:
        tf.config.experimental.set_memory_growth(device, True)
if gpus:
# Restrict TensorFlow to only allocate 2GB of memory on the first GPU
    try:
        tf.config.experimental.set_virtual_device_configuration(
            gpus[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1500)])
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Virtual devices must be set before GPUs have been initialized
        print(e)
else:
    print('no gpus')

def extract_features(model, image_paths):
    print(np.shape(image_paths))
    images = np.zeros((len(image_paths),224,224,3))
    for i, path in enumerate(image_paths):
        image = tf.keras.utils.load_img(path, target_size=(224,224))
        image = img_to_array(image)
        image = preprocess_input(image)
        images[i] = image
    
    features = model.predict(images)
    return features

def find_similar_images(features, image_paths):
    sim_scores = np.dot(features, np.transpose(features))
    for i in range(len(sim_scores)):
        sim_scores[i,i] = -1

    image_index = np.argmax(sim_scores, axis=1)
    similar_images = []
    for i, index in enumerate(image_index):
        if i == index:
            continue
        similar_images.append((image_paths[i], image_paths[index]))

    return similar_images

# Collect image path from the user
n = int(input('Give me the number of paths you want to include: '))
image_folder_paths = []
image_paths = []
types = ('*.png', '*.jpg', '*.jpeg')
for i in range(n):
    path = input('Enter the path: ')
    for typ in types:
        image_paths.extend(pathlib.Path(path).glob(typ))

print(np.shape(image_paths))
#image_paths = [...] # list of image paths
model = VGG16(weights='imagenet', include_top=False)

features = extract_features(model, image_paths)
similar_images = find_similar_images(features, image_paths)
