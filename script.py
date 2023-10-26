from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Node:
    def __init__(self,data):
        self.left=None
        self.right=None
        self.data=data

    def insert(self,data):
        pass
    

    

def getCredentials():
    file = open("credentials","r")
    user = file.readline()
    password = file.readline()
    file.close()
    return user.strip(), password.strip()

def login(user,parola):
    options = Options()
    browser = Firefox(options=options)
    browser.get("https://www.pbinfo.ro")

    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button.fc-button.fc-cta-do-not-consent.fc-secondary-button[aria-label='Do not consent']"))).click()

    browser.find_element(By.LINK_TEXT,"Autentificare").click()

    username=browser.find_element(By.ID,"user_login")
    password=browser.find_element(By.ID,"parola_login")
    username.send_keys(user)
    password.send_keys(parola)

    browser.find_element(By.CSS_SELECTOR,"button.btn.btn-primary").click()
    return browser

def getProblemID():
    file = open("test.cpp","r")
    problemNr = file.readline()[2:].strip()
    problemName = file.readline()[2:].strip()
    file.close()
    return problemNr, problemName

def getSourceCode():
    file = open("test.cpp","r")
    source = file.read()
    file.close()
    startIndex=source.find("#")
    source = source[startIndex:]

    return source

def submitCode(browser):
    problemNr, problemName= getProblemId()
    sourceCode = getSourceCode()
    problemURL="https://www.pbinfo.ro/probleme/"+problemNr+"/"+problemName
    browser.get(problemURL)
    sourceArea = browser.find_element(By.ID,"sursa")
    sourceArea.send_keys(sourceCode)
    submitButton = browser.find_element(By.ID,"btn-submit")
    submitButton.click()


user, parola = getCredentials()
#browser=login(user,parola)
#submitCode(browser)
getSourceCode()



