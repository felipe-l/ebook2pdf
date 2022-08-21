from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
from fake_useragent import UserAgent
import time
import python3_utils
import os
from PIL import Image
import pickle

Image.MAX_IMAGE_PIXELS = 5000000000

#!TODO Save book pngs in dedicated folder

def openBrowser():
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--start-maximized");

    # Recommended: This option is useful to avoid ban, saves cookies in profile
    options.add_argument(r"--user-data-dir=C:\Users\pipec\AppData\Local\Google\Chrome\User Data")  # e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
    options.add_argument(r'--profile-directory=Profile3')  # e.g. Profile 3

    options.add_argument(f'user-agent={userAgent}')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://chegg.com")
    input("SIGN IN TO CHEGG, GO TO FIRST PAGE OF BOOK AND MAXIMIZE WINDOW, press enter when finished")
    return driver

def cropBookPage(fileName, saveName, bookName):
    from PIL import Image

    im = Image.open(os.getcwd() + "/" + bookName + "/png/" + fileName)
    width, height = im.size
    viewportWidth = 1920
    # Setting the points for cropped image
    left = (viewportWidth - 990)/2
    top = 0
    right = width-((viewportWidth - 990)/2)
    bottom = height

    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((left, top, right, bottom))
    im1.save(os.getcwd() + "/" + bookName + "/png/" + saveName)
    os.remove(os.getcwd() + "/" + bookName + "/png/" + fileName)

def fullpage_screenshot(driver, file, heightScroll, bookName):
    print("Starting chrome full page screenshot workaround ...")

    screenWidth = 1920

    total_width = screenWidth
    #total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    total_height = int(heightScroll)
    if total_height < 969:
        #For pages smaller than viewport
        total_height = 969

    #viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_width = screenWidth
    #viewport_height = driver.execute_script("return window.innerHeight")
    viewport_height = 969
    print("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height, viewport_width, viewport_height))
    rectangles = []

    i = 0
    while i < total_height:
        ii = 0
        top_height = i + viewport_height

        if top_height > total_height:
            top_height = total_height

        while ii < total_width:
            top_width = ii + viewport_width

            if top_width > total_width:
                top_width = total_width

            print("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
            rectangles.append((ii, i, top_width, top_height))

            ii = ii + viewport_width

        i = i + viewport_height

    stitched_image = Image.new('RGB', (total_width, total_height))
    previous = None
    part = 0

    for rectangle in rectangles:
        if not previous is None:
            driver.execute_script("window.scrollTo({0}, {1})".format(0, rectangle[1]))
            print("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
            time.sleep(0.5)

        file_name = "part_{0}.png".format(part)
        print("Capturing {0} ...".format(file_name))

        driver.get_screenshot_as_file(file_name)
        screenshot = Image.open(file_name)

        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])

        print("Adding to stitched image with offset ({0}, {1})".format(offset[0], offset[1]))
        stitched_image.paste(screenshot, offset)

        del screenshot
        os.remove(file_name)
        part = part + 1
        previous = rectangle

    print(file)
    stitched_image.save(os.getcwd() + "/" + bookName + "/png/" + file)

    driver.execute_script("""
    var allButtons = document.querySelectorAll("button");
    allButtons[allButtons.length-1].click();
    """)

    print("Finishing chrome full page screenshot workaround...")

    fileName = file.split("temp.")[0]
    cropBookPage(file, fileName + ".png", bookName)
    time.sleep(5)
    return True


def takeScreenshot(bookName, startingPage):
    if not os.path.exists(os.getcwd() + "/" + bookName):
        # if the demo_folder directory is not present
        # then create it.
        os.makedirs(os.getcwd() + "/" + bookName)
        os.makedirs(os.getcwd() + "/" + bookName + "/png")
        os.makedirs(os.getcwd() + "/" + bookName + "/pngTrim")
        os.makedirs(os.getcwd() + "/" + bookName + "/pdf")


    # # Opening JSON file
    # with open('browserId.json', 'r') as openfile:
    #     browser = json.load(openfile)
    # url = browser["url"]
    # session_id = browser["session_id"]
    #
    # driver = webdriver.Remote(command_executor=url, desired_capabilities={})
    # driver.close()
    # driver.session_id = session_id

    driver = openBrowser()

    #deleteCheggNav
    driver.execute_script('''
    function getElementByXpath(path) {
        return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    }

    const nav = getElementByXpath("/html/body/div/div/section[1]");
    const content = getElementByXpath("/html/body/div/div/section[3]");
    const footer = getElementByXpath("/html/body/div/div/section[5]");
    
    footer.remove();
    nav.remove();
    content.style.top = 0;
    content.style.bottom = 0;
    ''')

    currPage = startingPage
    driver.switch_to.frame(driver.find_element(By.XPATH, "/html/body/div/div/section[2]/section/iframe"))
    input("ARE YOU READY TO PRINT ALL PAGES?")

    # While there is a next page button
    while (driver.execute_script("""
    var allButtons = document.querySelectorAll("button");
    return allButtons[allButtons.length-1].classList.contains("next");
    """)):
        driver.execute_script("window.scrollTo(0,0)")
        height = driver.find_element(By.TAG_NAME, "main").size["height"]
        width = driver.find_element(By.TAG_NAME, "main").size["width"]

        #make Buttons invisible, cannot delete to go to next page
        driver.execute_script("""
        var allButtons = document.querySelectorAll("button");
        for (var y = 0; y < allButtons.length; y++){
            allButtons[y].style.cssText = "margin: 0 !important; padding: 0 !important; height: 0 !important; border: 0 !important;";
            allButtons[y].innerHTML = "";
        }
        """)

        fullpage_screenshot(driver, str(currPage)+"temp.png", height, bookName)
        currPage += 1

# !TODO DELETE FUNCTION
# def getSession():
#
#     options = Options()
#     ua = UserAgent()
#     userAgent = ua.random
#     print(userAgent)
#     options.add_argument(f'user-agent={userAgent}')
#     options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     options.add_experimental_option('useAutomationExtension', False)
#     options.add_argument('--disable-blink-features=AutomationControlled')
#     driver = webdriver.Chrome(chrome_options=options)
#
#     url = driver.command_executor._url  # "http://127.0.0.1:60622/hub"
#     session_id = driver.session_id  # '4e167f26-dc1d-4f51-a207-f761eaf73c31'
#
#     browserId = {
#         "url": url,
#         "session_id": session_id
#     }
#     json_object = json.dumps(browserId, indent=4)
#     with open("browserId.json", "w") as outfile:
#         outfile.write(json_object)
#     driver.get("https://google.com")
#     options.add_experimental_option("detach", True)
#     print("done")
