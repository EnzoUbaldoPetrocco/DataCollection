import imagehash
from PIL import Image

def find_similar_images(image_paths):
    images = {}
    for path in image_paths:
        image = Image.open(path)
        hash = str(imagehash.phash(image))
        if hash in images:
            images[hash].append(path)
        else:
            images[hash] = [path]

    return [v for v in images.values() if len(v) > 1]
