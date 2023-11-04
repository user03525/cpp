import curses
import math

class Line():
    def __init__(self,line):
        self.line=line
        self.size = len(line)
        self.rows=1

    def update(self,screen):
        _ , width = screen.getmaxyx()
        ratio = self.size//width
        self.rows = int(math.ceil(self.size/width))

    def draw(self,console):
        console.screen.addstr(console.i,0,console.sign+self.line)
        self.update(console.screen)
        return console.i+self.rows

    def getString(self):
        return self.line

class Console():
    def __init__(self):
        self.screen = curses.initscr()
        self.screen.keypad(True)
        self.lines=[]
        self.sign = "<?> "
        self.currentLine = "" 
        self.lineNumber=0
        self.UP_CODE=259
        self.DOWN_CODE=258
        self.DELETE_CODE=127
        self.i=0
        self.handler=None

    def addHandler(self,handler):
        self.handler=handler

    def put(self,string):
        line = Line(string)
        self.lines.append(line);
        self.currentLine=""
        self.lineNumber=len(self.lines)

    def pop(self):
        self.lines.pop()
        self.lineNumber=len(self.lines)

    def draw(self):
        self.screen.clear()
        self.i=0
        for line in self.lines:
            self.i = line.draw(self)
        self.screen.addstr(self.i,0,self.sign+self.currentLine)
        self.screen.refresh()
   
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
                    self.lineNumber-=1
                    size = len(self.lines)
                    if self.lineNumber<0:
                        self.lineNumber=0
                    if size!=0:
                        self.currentLine=self.lines[self.lineNumber].getString()
                    self.draw()

                elif c==curses.KEY_DOWN or ord(c)==self.DOWN_CODE:
                    self.lineNumber+=1
                    size = len(self.lines)
                    if self.lineNumber>=size:
                        self.lineNumber=size-1
                        self.currentLine="" 
                    else:
                        self.currentLine=self.lines[self.lineNumber].getString()
                    self.draw()
                else:
                    self.currentLine+=c
            if self.handler != None:
                self.handler(self,self.currentLine)
            self.put(self.currentLine)
        curses.endwin()

    def print(msg):
        pass

def execute(console,command):
    if command=="exit":
        quit()
    elif command=="print":
        console.print("test gud")
        

console = Console()
console.addHandler(execute)
console.update()
