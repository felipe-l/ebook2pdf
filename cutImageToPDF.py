import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = 50000000000
import os
import shutil


def cutImages(mergeImages, bookName):
    images = [Image.open(os.getcwd() + "/" + bookName + "/png/" + x) for x in mergeImages]

    if os.path.exists(os.getcwd() + "/" + bookName + "/pngTrim"):
        shutil.rmtree(os.getcwd() + '/' + bookName + "/pngTrim")
        os.makedirs(os.getcwd() + "/" + bookName + "/pngTrim")
    else:
        os.makedirs(os.getcwd() + "/" + bookName + "/pngTrim")

    # The Height the images will be cut at
    cutHeight = 1122
    # currPage is used as a counter to name files
    currPg = 1
    for im in images:
        # This loop will cut an image by cutHeight and save the crop
        # when it cannot crop a full size it will terminate on that last iteration.
        width, height = im.size

        if height > cutHeight:
            currHeight = 0
            while height > cutHeight:
                print(height, currHeight, currHeight + cutHeight)
                im1 = im.crop((0, currHeight, width, currHeight + cutHeight))
                im1.save(os.getcwd() + "/" + bookName + "/pngTrim/" + str(currPg) + ".png")
                currHeight += cutHeight
                height -= cutHeight
                currPg += 1
            im1 = im.crop((0, currHeight, width, currHeight + cutHeight))
            im1.save(os.getcwd() + "/" + bookName + "/pngTrim/" + str(currPg) + ".png")
            currPg += 1
        else:
            currHeight = 0
            im1 = im.crop((0, currHeight, width, currHeight + cutHeight))
            im1.save(os.getcwd() + "/" + bookName + "/pngTrim/" + str(currPg) + ".png")
            currPg += 1

def gatherImageNames(bookName):
    mergeImages = []
    currCount = 0
    for file in os.listdir(os.getcwd() + "/" + bookName + "/png"):
        if file.endswith(".png"):
            mergeImages.append(file)
        currCount += 1
    print("TOTAL IMAGES:", str(currCount))

    #This file works only with numbered name images, to properly sort ex:1.png is first page
    mergeImages = sorted(mergeImages)
    return mergeImages

# mergeImages = gatherImageNames("book")
# print(mergeImages)
# input("Start Cropping above images")
# cutImages(mergeImages)