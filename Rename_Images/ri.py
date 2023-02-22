import os
import pathlib

n = int(input('Give me the number of paths you want to include: '))
base = input(' Give me the base name of the images: ')
destination = input('Give me the destination where to put the images: ')

if not os.path.exists(destination):
    print(f'Making directory: {str(destination)}')
    os.makedirs(destination)

image_folder_paths = []
image_paths = []
types = ('*.png', '*.jpg', '*.jpeg')
for i in range(n):
    path = input('Enter the path: ')
    for typ in types:
        image_paths.extend(pathlib.Path(path).glob(typ))
for i in range(len(image_paths)):
    path = ''
    directories = str(image_paths[i]).split('\\\\')
    for j in directories:
        path = path + j
    os.rename(str(path), destination +'/' + f'image_{i}.jpeg')