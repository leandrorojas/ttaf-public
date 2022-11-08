#!/usr/bin/python3

from datetime import date, timedelta, datetime
from os import path
from sys import argv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import pyotp

#TODO: to store password locally and encrypted
#import keyring

#const
__ARG_DATE_FORMAT = "%Y-%m-%d"
__PAGE_DATE_FORMAT = "%m/%d/%Y"
__HOURS_TO_LOG = "8"
#keyring app id
#__APP_ID = "tts"

__USERNAME = ""
__GOOGLE_PASSWORD = ""

#var
execute = False
#debugMode
debugMode = True
#debugMode = False

def isEoM(toCheck):
    todayMonth = toCheck.month
    tommorrowMonth = (toCheck + timedelta(days = 1)).month
    return todayMonth != tommorrowMonth

def isDayFriday(toCheck):
    return toCheck.weekday() == 4

def setTextByID(browser, id, text):
    inputElement = browser.find_element(By.ID, id)
    inputElement.send_keys(text)

def setTextByXPath(browser, xpath, text):
    waitForItemVisible(browser, xpath)
    inputElement = browser.find_element(By.XPATH, xpath)
    inputElement.send_keys(text)

def clickElementByXPath(browser, xpath):
    browser.execute_script("arguments[0].click();", WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))))

def waitForItemVisible(browser, xpath):
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))

def waitForItemPresence(browser, xpath):
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

def waitForItemToHide(browser, elementID):
    WebDriverWait(browser, 10).until(EC.invisibility_of_element((By.ID, elementID)))

def waitForItemToHideByXPath(browser, xpath):
    WebDriverWait(browser, 10).until(EC.invisibility_of_element((By.XPATH, xpath)))

def getTextByXPath(browser, xpath):
    waitForItemPresence(browser, xpath)
    return browser.find_element(By.XPATH, xpath).text

def getTextFromInputByXPath(browser, xpath):
    inputBox = browser.find_element(By.XPATH, xpath)
    return inputBox.get_attribute("value")

def clearInputByXPath(browser, xpath):
    browser.find_element(By.XPATH, xpath).clear()

def debugPrinting(message):
    global debugMode

    if (debugMode == True):
        print(message)

def printDateAndTime(additionalMessage = ""):
    print("[" + str(datetime.now())[:-3] + "] " + additionalMessage)

printDateAndTime("starting...")

if (len(argv) == 2):
    today = datetime.strptime(argv[1], __ARG_DATE_FORMAT)
else:
    #get date
    today = date.today()

#TODO: research if there is a way to load the default Chrome profile to skip google's 2 factor authentication

# EoM? fill
if (isEoM(today) == True):
    debugPrinting("it's EoM")
    execute = True
else:
    # Friday? fill
    if (isDayFriday(today) == True):
        debugPrinting("it's Friday")
        execute = True

if (execute == True):
    # chromeOptions = Options()
    # chromeOptions.add_argument("--headless")
    #TODO: deal with "DeprecationWarning: executable_path has been deprecated, please pass in a Service object"
    browser = webdriver.Chrome(path.join(path.dirname(path.realpath(__file__)), "chromedrivers/chromedriver_linux64")) # , options = chromeOptions)
    debugPrinting("browser created")

    # open web page
    browser.get("https://time.fortegrp.com/#/my-time")
    debugPrinting("login opened")
    # TTS login
    setTextByXPath(browser, "/html/body/ui-view/div/div/div[2]/div/div/div/div/form/div[1]/input", __USERNAME)

    clickElementByXPath(browser, "/html/body/ui-view/div/div/div[2]/div/div/div/div/form/div[2]/button") 
    clickElementByXPath(browser, "/html/body/div[1]/div/div/form/div[3]/button")
    debugPrinting("login completed")

    debugPrinting("starting google login")
    #google login
    setTextByXPath(browser, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input", __USERNAME)
    clickElementByXPath(browser, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button")
    setTextByXPath(browser, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input", __GOOGLE_PASSWORD)
    clickElementByXPath(browser, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button")

    #TODO: add try and do loop until the page is loaded, then remove the sleep line
    debugPrinting("google login finished")
    mainPageLoaded = False

    while(mainPageLoaded == False):
        try:
            waitForItemPresence(browser, "/html/body/ui-view/div/div/div[2]/div[2]/div/div/form/div[2]/div/div/div[1]/table/tbody/tr/th/div[1]")
            mainPageLoaded = True
        except:
            mainPageLoaded = False

    #TODO: get list of current month holidays
    
    filled = False
    currentRow = 1

    # date <= today?

    debugPrinting("starting autofilling")
    while(filled == False):
        rawText = getTextByXPath(browser, "/html/body/ui-view/div/div/div[2]/div[2]/div/div/form/div[2]/div/table/tbody/tr[" + str(currentRow) + "]/td[1]/div")

        dateInPage = datetime.strptime(rawText[4:], __PAGE_DATE_FORMAT).date()

        currentHours = int(getTextFromInputByXPath(browser, "/html/body/ui-view/div/div/div[2]/div[2]/div/div/form/div[2]/div/table/tbody/tr[" + str(currentRow) + "]/td[3]/input"))

        #if empty, fill
        if (currentHours == 0):
            currentRowXPath = "/html/body/ui-view/div/div/div[2]/div[2]/div/div/form/div[2]/div/table/tbody/tr[" + str(currentRow) + "]/td[3]/input"
            clearInputByXPath(browser, currentRowXPath)
            setTextByXPath(browser,currentRowXPath , __HOURS_TO_LOG)

        if (today == dateInPage):
            #save
            clickElementByXPath(browser, "/html/body/ui-view/div/div/div[2]/div[2]/div/div/form/div[1]/div/button")
            filled = True
        else:
            currentRow = currentRow + 1

    browser.close()
    print("browser killed")

printDateAndTime("finished!")