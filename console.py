import curses
import math

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

class Prompter():
    def __init__(self,console):
        self.lines=[]
        self.console=console
        self.startIndex=0
        self.height , self.width = self.console.screen.getmaxyx()

    def update(self):
        self.height , self.width = self.console.screen.getmaxyx()
        self.lines.clear()
        for line in self.console.lines:
            for token in line.tokens:
                self.lines.append(self.console.sign+token if line.command else token)
        self.size=len(self.lines)
        self.startIndex=max(self.size-self.height,0)

    def draw(self):
        self.console.screen.clear()
        for i in range(self.height):
            if i+self.startIndex>=0 and i+self.startIndex<self.size:
                self.console.screen.addstr(i,0,self.lines[i+self.startIndex])
            else:
                break
        self.console.screen.refresh()
        return i

    def scrollUp(self):
        #if self.startIndex>0:
        self.startIndex-=1

    def scrollDown(self):
        #if self.size-self.startIndex<self.height:
        self.startIndex+=1

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
        self.scroll=0
        self.blockScrollUp=False
        self.blockScrollDown=False
        self.prompter=Prompter(self)

    def clear(self):
        self.lines.clear()

    def addHandler(self,handler):
        self.handler=handler

    def put(self,string):
        line = Line(string)
        self.lines.append(line);
        self.currentLine=""
        self.lineNumber=len(self.lines)
        height , _ = self.screen.getmaxyx()
        self.scroll=0
        #self.blockScrollUp=False
        #self.blockScrollDown=False
        
        
    def pop(self):
        self.lines.pop()
        self.lineNumber=len(self.lines)

    def drawHistory(self):
        self.prompter.update()
        return self.prompter.draw()

    def draw(self):
        self.i = self.drawHistory()
        height , _ = self.screen.getmaxyx()
        if self.i<height:
            self.screen.addstr(self.i,0,self.sign+self.currentLine)
            self.screen.refresh()

    def update(self):
        command=""
        while True:
            self.drawHistory()
            if self.handler != None:
                self.handler.execute(command)
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
                    self.draw()
                elif ord(c)==self.PAGE_DOWN_CODE:
                    self.prompter.scrollDown()
                    self.draw()
                else:
                    #self.currentLine+=str(ord(c))
                    self.currentLine+=c
            command=self.currentLine
            self.put(self.currentLine)

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
