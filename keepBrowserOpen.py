from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
from fake_useragent import UserAgent
import pickle
import time

def importCookies(driver):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

def getSession():

    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')

    options.add_argument(r"--user-data-dir=C:\Users\pipec\AppData\Local\Google\Chrome\User Data")  # e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
    options.add_argument(r'--profile-directory=Profile3')  # e.g. Profile 3
    #options.add_argument("--headless")
    #options.add_argument("--window-size=%s" % "1920,1080")
    options.add_argument(f'user-agent={userAgent}')
    driver = webdriver.Chrome(chrome_options=options)

    url = driver.command_executor._url  # "http://127.0.0.1:60622/hub"
    session_id = driver.session_id  # '4e167f26-dc1d-4f51-a207-f761eaf73c31'

    browserId = {
        "url": url,
        "session_id": session_id
    }

    json_object = json.dumps(browserId, indent=4)
    with open("browserId.json", "w") as outfile:
        outfile.write(json_object)

    driver.get("https://google.com")
    options.add_experimental_option("detach", True)
    print("done")
    while True:
        pass


#
# getSession()