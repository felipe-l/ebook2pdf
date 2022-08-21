from PIL import Image
Image.MAX_IMAGE_PIXELS = 50000000000
import os

def sortImageNames():
    mergeImages = []
    for file in os.listdir(os.getcwd() + "/book"):
        if file.endswith(".png"):
            mergeImages.append(int(file.split(".")[0]))
    mergeImages = sorted(mergeImages)
    print(mergeImages)
    return mergeImages

def createPDF(imageNames):
    images = [Image.open(os.getcwd() + "/book/" + str(x) + ".png").convert('RGB') for x in imageNames]
    images[0].save(r'mergedImages.pdf', save_all=True, append_images=images[1:])


imageNames = sortImageNames()
input("Press Enter to create PDF")
createPDF = createPDF(imageNames)


