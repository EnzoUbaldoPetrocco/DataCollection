import os
import pathlib

n = int(input('Give me the number of paths you want to include: '))
base = input(' Give me the base name of the images: ')
destination = input('Give me the destination where to put the images: ')
image_folder_paths = []
image_paths = []
types = ('*.png', '*.jpg', '*.jpeg')
for i in range(n):
    path = input('Enter the path: ')
    for typ in types:
        image_paths.extend(pathlib.Path(path).glob(typ))
for i in range(len(image_paths)):
    os.rename(image_paths[i], destination +'/' + f'image_{i}.jpeg')