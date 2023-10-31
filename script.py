from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re
import time

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

def getTokens(source):
    includes = []
    prototypes = []
    main = ""
    functions = []
    tokens = source.split("\n")
    for i in range(len(tokens)):
        if tokens[i].startswith("#include<") or tokens[i].startswith("using"):
            includes.append(tokens[i])
        elif tokens[i].startswith("int main"):
            stack = []
            stack.append('{')
            main+=tokens[i]
            main+="\n"
            while stack:
                i=i+1
                for c in tokens[i]:
                    if c == '{':
                        stack.append(c)
                    elif c=='}':
                        stack.pop()
                main+=tokens[i]
                main+="\n"
        elif re.search("[a-zA-Z_0-9]+ [a-zA-Z_0-9]+\(.+\);",tokens[i]):
            prototypes.append(tokens[i])
        elif re.search("[a-zA-Z_0-9]+ [a-zA-Z_0-9]+\(.+\)",tokens[i]):
            stack = []
            stack.append('{')
            function=tokens[i]
            function+="\n"
            while stack:
                i=i+1
                for c in tokens[i]:
                    if c == '{':
                        stack.append(c)
                    elif c=='}':
                        stack.pop()
                function+=tokens[i]
                function+="\n"
            functions.append(function)
    return includes, prototypes, main, functions

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
    includes, prototypes, main, functions = getTokens(source)

    file = open("hogwarts.h","r")
    source = file.read()
    file.close()
    hIncludes, hPrototypes, _, _= getTokens(source)

    file = open("hogwarts.cpp","r")
    source = file.read()
    file.close()
    lIncludes, _, _, lFunctions = getTokens(source)
    
    allIncludes = sorted(set(hIncludes+lIncludes+includes))
    allPrototypes = getAllPrototypes(prototypes+hPrototypes,[main]+functions)
    allFunctions = getAllFunctions(allPrototypes,functions+lFunctions)
    
    finalSource = ""
    for item in allIncludes:
        finalSource += item
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
    #print(finalSource)

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

def console():
    while True:
        print("c=3 ",end="")
        command = input()
        if command == "connect":
            user, parola = getCredentials()
            browser=login(user,parola)
            print("connected")
        elif command == "submit": 
            submitCode(browser)
            print("code submited")
        elif command == "exit":
            return



console()


