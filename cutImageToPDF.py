import sys
from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = 50000000000

import os
mergeImages = []
currCount = 0
for file in os.listdir(os.getcwd()):
    if file.endswith(".png"):
        print(currCount)
        mergeImages.append(file)
    currCount += 1
mergeImages = sorted(mergeImages)
print(mergeImages)

input()

images = [Image.open(x) for x in mergeImages]
# images = [Image.open("akpg0F.png")]
# im = Image.open("akpg1F.png")

currPg = 1
for im in images:
    width, height = im.size

    if height > 1122:
        currHeight = 0
        while height > 1122:
            print(height, currHeight, currHeight+1122)
            im1 = im.crop((0, currHeight, width, currHeight+1122))
            im1.save(os.getcwd() + "/book/" + str(currPg) + ".png")
            currHeight += 1122
            height -= 1122
            currPg += 1
        im1 = im.crop((0, currHeight, width, currHeight+1122))
        im1.save(os.getcwd() + "/book/" + str(currPg) + ".png")
        currPg += 1
    else:
        currHeight = 0
        im1 = im.crop((0, currHeight, width, currHeight+1122))
        im1.save(os.getcwd() + "/book/" + str(currPg) + ".png")
        currPg += 1