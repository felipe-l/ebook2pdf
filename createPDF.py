from PIL import Image
Image.MAX_IMAGE_PIXELS = 50000000000
import os

def sortImageNames(bookName):
    mergeImages = []
    for file in os.listdir(os.getcwd() + "/" + bookName + "/pngTrim"):
        if file.endswith(".png"):
            mergeImages.append(int(file.split(".")[0]))
    mergeImages = sorted(mergeImages)
    print(mergeImages)
    return mergeImages

def createPDF(imageNames, bookName):
    images = [Image.open(os.getcwd() + "/" + bookName + "/pngTrim/" + str(x) + ".png").convert('RGB') for x in imageNames]
    # !TODO CHANGE SAVE DIR
    images[0].save(os.getcwd() + "/" + bookName + "/pdf/" + bookName + ".pdf", save_all=True, append_images=images[1:])


# imageNames = sortImageNames()
# input("Press Enter to create PDF")
# createPDF = createPDF(imageNames)


