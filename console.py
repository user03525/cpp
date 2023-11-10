import curses
import math

class Line():
    def __init__(self,line,sign=True):
        self.line=line
        self.size = len(line)
        self.sign=sign
        self.rows=1

    def getNrRows(self,screen):
        _ , width = screen.getmaxyx()
        ratio = self.size//width
        self.rows = int(math.ceil(self.size/width))
        return self.rows

    def draw(self,console):
        self.getNrRows(console.screen)
        console.screen.addstr(console.i,0,console.sign+self.line if self.sign else self.line)
        return console.i+self.rows

    def getString(self):
        return self.line



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
        self.DELETE_CODE=127
        self.i=0
        self.handler=None
        self.scroll=0

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
        if self.lineNumber>=height:
            self.scroll=self.lineNumber-height
        
    def pop(self):
        self.lines.pop()
        self.lineNumber=len(self.lines)

    def drawHistory(self):
        self.screen.clear()

        drawHeight=0
        for line in self.lines:
            drawHeight+=line.getNrRows(self.screen)

        height , _ = self.screen.getmaxyx()
        lineIndex = 0

        while drawHeight>=height:
            drawHeight-=self.lines[lineIndex].getNrRows(self.screen)
            lineIndex+=1
        
        self.i=0;
        while lineIndex<len(self.lines):
            self.i = self.lines[lineIndex].draw(self)
            lineIndex+=1
        self.screen.refresh()

    def draw(self):
        self.drawHistory()
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
            command=self.currentLine
            self.put(self.currentLine)
        curses.endwin()

    def print(self,*args):
        if type(args[0])==list:
            for item in args[0]:
                self.lines.append(Line(item,sign=False))
        elif args[0] is None:
            self.lines.append(Line("None",sign=False))
        else:
            msg=" ".join(args)
            for line in msg.split("\n"):
                self.lines.append(Line(line,sign=False))


if __name__ == "__main__":    
    def execute(console,command):
        if command=="exit":
            quit()
        elif command.startswith("print"):
            console.print(command[command.find(" ")+1:])
        elif command=="clear":
            console.clear()
            

    console = Console()
    console.addHandler(execute)
    console.update()
