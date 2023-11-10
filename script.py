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
from function import Function

class Handler():
    def __init__(self,console):
        self.console=console
        self.browser=None

    def getCredentials(self):
        file = open("credentials","r")
        user = file.readline()
        password = file.readline()
        file.close()
        return user.strip(), password.strip()

    def login(self,user,parola):
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

    def getProblemID(self):
        file = open("test.cpp","r")
        problemNr = file.readline()[2:].strip()
        problemName = file.readline()[2:].strip()
        file.close()
        return problemNr, problemName

    def readFunction(self,tokens,i):
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


    def getTokens(self,source):
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
                main = self.readFunction(tokens,i)
            elif re.search("template",tokens[i]):
                templates.append(self.readFunction(tokens,i))
            elif re.search("(?!return)(?<![a-zA-Z])(([a-zA-Z_0-9<>,]+) [a-zA-Z_0-9]+\(.+\));",tokens[i]):
                prototypes.append(tokens[i])
            elif re.search("(?!return)(?<![a-zA-Z])(([a-zA-Z_0-9<>,]+) [a-zA-Z_0-9]+\(.+\))",tokens[i]):
                functions.append(self.readFunction(tokens,i))
        return includes, prototypes, main, functions, templates

    def getFunctionName(self,text):
        indexStart = text.find(" ")
        indexFinal = text.find("(")
        return text[indexStart+1:indexFinal]

    def getTemplateName(self,template):
        indexStart = template.find(">")
        indexFinal = template.find("(")
        indexStart+=1
        while template[indexStart]==" ":
            indexStart+=1
        return template[indexStart:indexFinal].split(" ")[1]

    def getAllPrototypes(self,prototypes,foundPrototypes,main, functions,lFunctions):
        prototypes=list(set(prototypes))
        allPrototypes = []
        usedFunctions = []
        for prototype in prototypes:
            for function in functions+[main]:
                functionName = self.getFunctionName(prototype) 
                if functionName in function:
                    allPrototypes.append(prototype)

        allPrototypes=list(set(allPrototypes))

        for prototype in allPrototypes:
            for function in functions+lFunctions:
                if self.getFunctionName(prototype) in self.getFunctionName(function):
                    usedFunctions.append(function)

        usedFunctions=list(set(usedFunctions))
        
        if sorted(foundPrototypes) != sorted(allPrototypes):
            return self.getAllPrototypes(prototypes,allPrototypes,main,usedFunctions,lFunctions)
        else:
            return allPrototypes

    def getAllFunctions(self,prototypes,functions):
        allFunctions = []
        for prototype in prototypes:
            for function in functions:
                if self.getFunctionName(prototype) in self.getFunctionName(function):
                    allFunctions.append(function)
                    break
        return allFunctions

    def getAllTemplates(self,templates,functions):
        allTemplates = []
        for template in templates:
            for function in functions:
                templateName = self.getTemplateName(template) 
                if templateName in function:
                    allTemplates.append(template)
                    break
        return allTemplates


    def getSourceCode(self):
        file = open("test.cpp","r")
        source = file.read()
        file.close()
        startIndex=source.find("#")
        source = source[startIndex:]
        includes, prototypes, main, functions, templates = self.getTokens(source)

        file = open("hogwarts.h","r")
        source = file.read()
        file.close()
        hIncludes, hPrototypes, _, _, hTemplates = self.getTokens(source)

        file = open("hogwarts.cpp","r")
        source = file.read()
        file.close()
        lIncludes, _, _, lFunctions, _ = self.getTokens(source)


        allFunctionsText = hTemplates+templates+functions+lFunctions
        '''
        for i,function in enumerate(lFunctions):
            console.print(str(i)) 
            console.print(function)
        '''
        functionsList = []
        for functionText in allFunctionsText:
            functionsList.append(Function(functionText))

        tree = Function(main)
        tree.computeChildren(functionsList)
        
        allIncludes = sorted(set(hIncludes+lIncludes+includes))
        '''
        allPrototypes = self.getAllPrototypes(prototypes+hPrototypes,[],main,functions+templates+hTemplates,lFunctions)
        allFunctions = self.getAllFunctions(allPrototypes,functions+lFunctions)
        allTemplates = self.getAllTemplates(templates+hTemplates,[main]+allFunctions)
        '''
        allPrototypes = tree.getAllPrototypes()
        allFunctions = tree.getAllFunctions()
        '''
        for prototype in allPrototypes:
            console.print(prototype)
        for function in allFunctions: 
            console.print(function)
        '''

        finalSource = ""
        for include in allIncludes:
            finalSource += include
            finalSource += "\n"
        finalSource += "\n"
        for prototype in allPrototypes:
            finalSource += prototype
            finalSource += "\n"
        '''        
        for item in allTemplates:
            finalSource += item;
            finalSource += "\n"
        finalSource += "\n"
        finalSource += "\n"
        finalSource += main
        finalSource += "\n"
        '''
        for function in allFunctions:
            finalSource += function
            finalSource += "\n"
        finalSource += "\n"

        return finalSource
        #return "sursa"

    def submitCode(self,browser):
        problemNr, problemName= self.getProblemID()
        sourceCode = self.getSourceCode()
        problemURL="https://www.pbinfo.ro/probleme/"+problemNr+"/"+problemName
        self.browser.get(problemURL)
        self.browser.execute_script("document.getElementById('btn-submit').scrollIntoView();")

        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.ID,"btn-submit")))

        sourceAreas = self.browser.find_elements(By.TAG_NAME,"textarea")
        sourceAreas[1].send_keys(sourceCode)
        submitButton = browser.find_element(By.ID,"btn-submit")
        submitButton.click()


    def execute(self,command):
        if command == "connect":
            user, parola = self.getCredentials()
            self.browser = self.login(user,parola)
            console.print("connected")
        elif command == "submit": 
            if self.browser:
                self.submitCode(self.browser)
                console.print("code submited")
            else:
                console.print("not connected")
        elif command == "source":
            console.print(self.getSourceCode())
            #self.getSourceCode()
        elif command == "id":
            console.print(*self.getProblemID())
        elif command == "exit":
            self.browser.quit()
            quit()
        elif command.startswith("print"):
            console.print(command[command.find(" ")+1:])
        elif command=="clear":
            console.clear()

console = Console()
console.addHandler(Handler(console))
console.update()


