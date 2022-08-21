BOOK_NAME = "myBook"
startingPage = 1

def bookToPdf(bookName, startingPage):
    import createPDF
    import cutImageToPDF
    import downloadBook

    downloadBook.takeScreenshot(BOOK_NAME, startingPage)
    print("BOOK DOWNLOADED")

    mergeImages = cutImageToPDF.gatherImageNames(BOOK_NAME)
    print(mergeImages)
    input("Start Cropping above images")
    cutImageToPDF.cutImages(mergeImages, BOOK_NAME)

    imageNames = createPDF.sortImageNames(BOOK_NAME)
    input("Press Enter to create PDF")
    createPDF = createPDF.createPDF(imageNames, BOOK_NAME)

if __name__ == "__main__":
    bookToPdf(BOOK_NAME, startingPage)