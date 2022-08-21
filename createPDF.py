import sys
from PIL import Image

Image.MAX_IMAGE_PIXELS = 50000000000

import os
mergeImages = []
for file in os.listdir(os.getcwd() + "/book"):
    if file.endswith(".png"):
        mergeImages.append(int(file.split(".")[0]))
mergeImages = sorted(mergeImages)
print(mergeImages)
images = [Image.open(os.getcwd() + "/book/" + str(x) + ".png").convert('RGB') for x in mergeImages]
input("YOU READY")
images[0].save(r'mergedImages.pdf',save_all=True,
append_images=images[1:])
