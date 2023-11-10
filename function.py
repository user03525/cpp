class Function():
    def __init__(self,functionText):
        self.children=[]
        self.functionText=functionText
        self.code=self.getCode(functionText)
        self.name=self.getName(functionText)
        self.visited=False
        self.prototype=self.getPrototype(functionText)

    def getAllPrototypes(self):
        prototypes=[]
        for child in self.children:
            prototypes+=child.getAllPrototypes()
        return prototypes+[self.prototype] if self.prototype != None else prototypes


    def getAllFunctions(self):
        functions=[]
        for child in self.children:
            functions+=child.getAllFunctions()
        return functions+[self.functionText]

    def computeChildren(self,functions):
        for function in functions:
            if not function.visited and function.name in self.code and function.name != self.name:
                function.visited=True
                self.children.append(function)
        for child in self.children:
            child.computeChildren(functions)

    def getCode(self,text):
        indexStart = text.find("{")
        return text[indexStart:]

    def getName(self,text):
        if "template" in text:
            indexStart = text.find(">")
            indexFinal = text.find("(")
            indexStart+=1
            while text[indexStart]==" ":
                indexStart+=1
            return text[indexStart:indexFinal].split(" ")[1]
        else:
            indexStart = text.find(" ")
            indexFinal = text.find("(")
            return text[indexStart+1:indexFinal]

    def getPrototype(self, text):
        if "template" in text or "main" in text:
            return None
        indexFinal = text.find("{")
        prototype = text[:indexFinal]
        prototype += ";"
        return prototype 
