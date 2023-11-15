import curses
import math
import textwrap

class Line():
    def __init__(self,line,command=True):
        self.line=line
        self.size = len(line)
        self.command=command
        self.tokens = self.line.split("\n")
        self.rows=1

    def getNrRows(self,screen):
        _ , width = screen.getmaxyx()
        self.rows=0
        for token in self.tokens:
            self.rows += self.getRowHeight(token,width)
        return self.rows

    def getRowHeight(self,row,width):
        return int(math.ceil(len(row)/width))

    def getString(self):
        return self.line
    
    def updateTokens(self,console):
        tokens=[]
        _ , width = console.screen.getmaxyx()
        if len(self.tokens)>0:
            index = width-len(console.sign)
            if index<len(self.tokens[0]):
                tokens.append(self.tokens[0][:index])
                tokens+=textwrap.wrap(self.tokens[0][index:],width)
            else:
                tokens.append(self.tokens[0])
        for i in range(1,len(self.tokens)):
            tokens+=self.getMultipleLines(self.tokens[i],width)
        self.tokens=tokens

    def getMultipleLines(self, token, width):
        return textwrap.wrap(token,width)


class Prompter():
    def __init__(self,console):
        self.lines=[]
        self.console=console
        self.startIndex=0
        self.height , self.width = self.console.screen.getmaxyx()

    def update(self):
        self.height , self.width = self.console.screen.getmaxyx()
        self.getLines()
        self.size=len(self.lines)
        self.startIndex=max(self.size-self.height+1,self.startIndex)

    def getLines(self):
        self.lines.clear()
        for line in self.console.lines:
            line.updateTokens(self.console)
            if len(line.tokens)>0:
                if line.command:
                    self.lines.append(self.console.sign+line.tokens[0])
                else:
                    self.lines.append(self.console.sign+line.tokens[0])
            for i in range(1,len(line.tokens)):
                self.lines.append(line.tokens[i])

    def draw(self):
        self.console.screen.clear()
        i = 0
        while i < self.height-1:
            if i+self.startIndex>=0 and i+self.startIndex<self.size:
                self.console.screen.addstr(i,0,self.lines[i+self.startIndex])
            else:
                break
            i+=1
        self.console.screen.addstr(i,0,self.console.sign+self.console.currentLine)
        self.console.screen.refresh()

    def scrollUp(self):
        self.height , self.width = self.console.screen.getmaxyx()
        self.getLines()
        self.size=len(self.lines)
        self.startIndex=max(self.startIndex-1,0)
        self.draw()

    def scrollDown(self):
        self.height , self.width = self.console.screen.getmaxyx()
        self.getLines()
        self.size=len(self.lines)
        self.startIndex=min(self.startIndex+1,self.size)
        self.draw()

class Console():
    def __init__(self):
        self.screen = curses.initscr()
        self.screen.keypad(True)
        self.screen.scrollok(True)
        self.lines=[]
        self.sign = "<?> "
        self.currentLine = "" 
        self.lineNumber=0
        self.UP_CODE=259
        self.DOWN_CODE=258
        self.LEFT_CODE=260
        self.RIGHT_CODE=261
        self.PAGE_UP_CODE=339
        self.PAGE_DOWN_CODE=338
        self.DELETE_CODE=127
        self.i=0
        self.handler=None
        self.blockScrollUp=False
        self.blockScrollDown=False
        self.prompter=Prompter(self)

    def clear(self):
        self.lines.clear()
        self.prompter.update()

    def addHandler(self,handler):
        self.handler=handler

    def put(self,string):
        line = Line(string)
        self.lines.append(line);
        self.lineNumber=len(self.lines)
        
    def pop(self):
        self.lines.pop()
        self.lineNumber=len(self.lines)

    def draw(self):
        self.prompter.update()
        self.prompter.draw()

    def update(self):
        while True:
            self.draw()
            while True:
                c = chr(self.screen.getch())
                if c==curses.KEY_ENTER or c=='\n' or c=='\r':
                    break
                elif c==curses.KEY_BACKSPACE or c==curses.KEY_DC or ord(c)==self.DELETE_CODE:
                    self.currentLine=self.currentLine[:-1]
                    self.draw()
                elif c==curses.KEY_UP or ord(c)==self.UP_CODE:
                    if self.lineNumber>0:
                        self.lineNumber-=1
                    while self.lineNumber>0 and not self.lines[self.lineNumber].command:
                        self.lineNumber-=1
                    if len(self.lines)!=0:
                        self.currentLine=self.lines[self.lineNumber].getString()
                    self.draw()

                elif c==curses.KEY_DOWN or ord(c)==self.DOWN_CODE:
                    self.lineNumber+=1
                    size = len(self.lines)
                    while self.lineNumber<size and not self.lines[self.lineNumber].command:
                        self.lineNumber+=1
                    if self.lineNumber>=size:
                        self.lineNumber=size-1
                        self.currentLine="" 
                    else:
                        self.currentLine=self.lines[self.lineNumber].getString()
                    self.draw()
                elif ord(c)==self.PAGE_UP_CODE:
                    self.prompter.scrollUp()
                elif ord(c)==self.PAGE_DOWN_CODE:
                    self.prompter.scrollDown()
                else:
                    #self.currentLine+=str(ord(c))
                    self.currentLine+=c
            self.put(self.currentLine)
            if self.handler != None:
                self.handler.execute(self.currentLine)
                self.draw()
            self.currentLine=""

    def print(self,*args):
        if type(args[0])==list:
            self.lines.append(Line(args[0].join(""),command=False))
        elif args[0] is None:
            self.lines.append(Line("None",command=False))
        else:
            msg=" ".join(args)
            #for line in msg.split("\n"):
            line = Line(msg,command=False)
            self.lines.append(line)

    def close(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()


if __name__ == "__main__":    
    def execute(console,command):
        if command=="exit":
            console.close()
            quit()
        elif command.startswith("print"):
            console.print(command[command.find(" ")+1:])
        elif command=="clear":
            console.clear()

    console = Console()
    console.addHandler(execute)
    console.update()
