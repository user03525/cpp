from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re
import time
import termios
import sys
import tty
import select
from console import Console

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

def readFunction(tokens,i):
    stack = []
    stack.append('{')
    function=tokens[i]
    function+="\n"
    while stack:
        i=i+1
        for c in tokens[i]:
            if c == '{':
                stack.append(c)
            elif c == '}':
                stack.pop()
        function+=tokens[i]
        function+="\n"
    return function


def getTokens(source):
    includes = []
    prototypes = []
    main = ""
    functions = []
    templates = []
    tokens = source.split("\n")
    for i in range(len(tokens)):
        if tokens[i].startswith("#include<") or tokens[i].startswith("using"):
            includes.append(tokens[i])
        elif tokens[i].startswith("int main"):
            main = readFunction(tokens,i)
        elif re.search("template",tokens[i]):
            templates.append(readFunction(tokens,i))
        elif re.search("(?!return)(?<![a-zA-Z])(([a-zA-Z_0-9<>,]+) [a-zA-Z_0-9]+\(.+\));",tokens[i]):
            prototypes.append(tokens[i])
        elif re.search("[a-zA-Z_0-9<>,]+ [a-zA-Z_0-9]+\(.+\)",tokens[i]):
            functions.append(readFunction(tokens,i))
    return includes, prototypes, main, functions, templates

def getFunctionName(text):
    indexStart = text.find(" ")
    indexFinal = text.find("(")
    return text[indexStart+1:indexFinal]

def getAllPrototypes(prototypes, functions):
    allPrototypes = []
    for prototype in prototypes:
        for function in functions:
            functionName = getFunctionName(prototype) 
            if functionName in function:
                allPrototypes.append(prototype)
                break
    return allPrototypes

def getAllFunctions(prototypes,functions):
    allFunctions = []
    for prototype in prototypes:
        for function in functions:
            if getFunctionName(prototype) in getFunctionName(function):
                allFunctions.append(function)
                break
    return allFunctions

def getSourceCode():
    file = open("test.cpp","r")
    source = file.read()
    file.close()
    startIndex=source.find("#")
    source = source[startIndex:]
    includes, prototypes, main, functions, templates = getTokens(source)

    file = open("hogwarts.h","r")
    source = file.read()
    file.close()
    hIncludes, hPrototypes, _, _, hTemplates = getTokens(source)

    file = open("hogwarts.cpp","r")
    source = file.read()
    file.close()
    lIncludes, _, _, lFunctions, _ = getTokens(source)
    
    allIncludes = sorted(set(hIncludes+lIncludes+includes))
    allTemplates = set(templates+hTemplates)
    allPrototypes = getAllPrototypes(prototypes+hPrototypes,[main]+functions)
    allFunctions = getAllFunctions(allPrototypes,functions+lFunctions)
    
    finalSource = ""
    for item in allIncludes:
        finalSource += item
        finalSource += "\n"
    finalSource += "\n"
    for item in allTemplates:
        finalSource += item;
        finalSource += "\n"
    finalSource += "\n"
    for item in allPrototypes:
        finalSource += item
        finalSource += "\n"
    finalSource += "\n"
    finalSource += main
    finalSource += "\n"
    for item in allFunctions:
        finalSource += item
        finalSource += "\n"
    finalSource += "\n"

    return finalSource

def submitCode(browser):
    problemNr, problemName= getProblemID()
    sourceCode = getSourceCode()
    problemURL="https://www.pbinfo.ro/probleme/"+problemNr+"/"+problemName
    browser.get(problemURL)
    browser.execute_script("document.getElementById('btn-submit').scrollIntoView();")

    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID,"btn-submit")))

    sourceAreas = browser.find_elements(By.TAG_NAME,"textarea")
    sourceAreas[1].send_keys(sourceCode)
    submitButton = browser.find_element(By.ID,"btn-submit")
    submitButton.click()

class Handler():
    def __init__(self,console):
        self.console=console
        self.browser=None

    def execute(self,command):
        if command == "connect":
            user, parola = getCredentials()
            self.browser=login(user,parola)
            console.print("connected")
        elif command == "submit": 
            if self.browser:
                submitCode(self.browser)
                console.print("code submited")
            else:
                console.print("not connected")
        elif command == "source":
            console.print(getSourceCode())
        elif command == "id":
            console.print(*getProblemID())
        elif command == "exit":
            quit()
        elif command.startswith("print"):
            console.print(command[command.find(" ")+1:])
        elif command=="clear":
            console.clear()

console = Console()
console.addHandler(Handler(console))
console.update()


