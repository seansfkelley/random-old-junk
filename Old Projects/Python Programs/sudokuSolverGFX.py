from graphics import *
from copy import deepcopy

def main(boardVar):
    """The main solving function."""
    board=deepcopy(boardVar)
    loc=[0,0]
    ##loc[0] is x, loc[1] is y
    iters=0
    if complete(board):
        return [board, 0]
    while True:
        loc=locChange(loc, board)
        iters+=1
        counter=[0]*9
        ##First checker line checks the location's row
        counter=checker(counter, board[loc[1]])
        ##Next line does column
        counter=checker(counter, getColumn(board, loc))
        ##Last line does group
        counter=checker(counter, getGroup(board, loc))
        zeroes=0
        zeroloc=0
        for i in range(9):
            ##for loop counts the number of zeroes and saves the last one's
            ##location within counter
            if counter[i]==0:
                zeroes+=1
                zeroloc=i
        if zeroes==1:
            ##If only one of the 9 counter values is a zero it must be the
            ##missing value (by process of elimination)
            board[loc[1]][loc[0]]=zeroloc+1
            if complete(board):
                ##Break the loop if this solved it
                break
        if iters==1000:
            ##Prevents infinite loops for unsolvable puzzles
            break
    return [board, iters]

def locChange(loc, board):
    """Returns the location of the next 0 in sequence."""
    redo=True
    while redo:
        loc[0]+=1
        if loc[0]==9:
            loc[1]+=1
            loc[0]=0
        if loc[1]==9:
            loc[1]=0
        if board[loc[1]][loc[0]]==0:
            redo=False
    return loc

def checker(counter, nums):
    """Checks how many of each value (1-9) are in nums. Inputs 1/0 (T/F) in counter accordingly."""
    for i in nums:
        if i!=0:
            counter[i-1]=1
    return counter

def getColumn(board, loc):
    """Returns a location's column."""
    column=loc[0]
    out=[]
    for i in range(9):
        out+=[board[i][column]]
    return out

def getGroup(board, loc):
    """Returns a location's group."""
    group=[]
    loc0=roundDown(loc[0])
    loc1=roundDown(loc[1])
    for i in range(loc0, loc0+3):
        for j in range(loc1, loc1+3):
            group+=[board[j][i]]
    return group

def roundDown(num):
    """Rounds num down to the nearest multiple of 3. All integers accepted."""
    while num%3:
        num-=1
    return num

def complete(board):
    """True/False check for completion."""
    for i in range(9):
        if 0 in board[i]:
            return False
    return True

def boardFormat(string):
    """Formats an 81-char string into a board variable. Use zeroes for blanks."""
    ret=[]
    for i in range(9):
        temp=[]
        for j in range(9):
            temp+=[int(string[i*9+j])]
        ret+=[temp]
    return ret

def printBoard(board):
    """Prints out the board neatly."""
    for i in range(9):
        for j in range(9):
            print board[i][j],
        print

def drawGrid(window):
    """Draws a 9x9 grid with 3x3 divisions on any size window."""
    temp=window.getHeight()/9
    for i in range(1,9):
        ##Vertical line loop
        lineTemp=Line(Point(0,temp),Point(window.getWidth(),temp))
        lineTemp.setFill('grey')
        ##Regular lines are light grey
        if not i%3:
            lineTemp.setWidth(2)
            lineTemp.setFill('black')
            ##Every 3 lines are thicker and darker to divide the 3x3 boxes
        lineTemp.draw(window)
        temp+=(window.getHeight()/9)
    temp=window.getWidth()/9
    for i in range(1,9):
        ##Horizontal line loop
        lineTemp=Line(Point(temp,0),Point(temp,window.getHeight()))
        lineTemp.setFill('grey')
        if not i%3:
            lineTemp.setWidth(2)
            lineTemp.setFill('black')
        lineTemp.draw(window)
        temp+=(window.getWidth()/9)

def drawBoard(window, board):
    """Draw the all the numbers to the window."""
    for i in range(9):
        for j in range(9):
            ##Loops pick every location and draw each with drawText()
            drawText(window, [i,j], board)

def drawText(window, loc, board):
    """Draws the number at a single location."""
    space=window.getWidth()/9.0
    tempText=Text(Point(loc[0]*space+space/2, loc[1]*space+space/2),\
                  str(board[loc[1]][loc[0]]))
    tempText.setSize(window.getWidth()/20)
    if tempText.getText()=='0':
        tempText.setText(' ')
    tempText.draw(window)

def convertToRC(window, point):
    """Converts a point into a row/column location."""
    x=point.getX()/(window.getHeight()/9)
    y=point.getY()/(window.getWidth()/9)
    return [x,y]

def solveText(board):
    """Solves and displays without using the graphics.py module."""
    ##Displays the board even if it's only partially solved
    solved=main(board)
    printBoard(solved[0])
    if not complete(solved[0]):
        print 'Error: Not completely solvable by this program.'
    else:
        print 'Success! Iterations:',solved[1]

def solve(board, winSize=400, winColor='white'):
    """Solve your Sudoku puzzle! winSize and winColor are window options."""
    ##Displays the board even if it's only partially solved
    window=GraphWin('Sudoku Solver', winSize, winSize)
    window.setBackground(winColor)
    drawGrid(window)
    solved=main(board)
    drawBoard(window, solved[0])
    if not complete(solved[0]):
        print 'Error: Not completely solvable by this program.'
    else:
        print 'Success! Iterations:',solved[1]

def hint(board, winSize=400, winColor='white'):
    """Get hints by clicking empty boxes to reveal the answer!"""
    hints=0
    solved=main(board)
    if not complete(solved[0]):
        ##hint() is useless if the board isnt completely solved:
        ##Doesnt open window or draw if it isnt solved
        print 'Error: Not completely solvable by this program.'
        print 'Use solve() for partial answers to unsolvable puzzles.'
        print 'hint() disabled.'
        return
    else:
        print 'Success! Iterations:',solved[1]
        print 'Click a space to reveal it.'
        print 'Click twice on any one space to end hint(), without revealing.'
        lastClick=[-1,-1]
        window=GraphWin('Sudoku Solver: Hints', winSize, winSize)
        window.setBackground(winColor)
        drawGrid(window)
        drawBoard(window, board)
    while True:
        click=convertToRC(window, window.getMouse())
        if lastClick==click:
            ##Check for double click
            break
        if not board[click[1]][click[0]]:
            ##Check if location is a zero, then draw the number
            drawText(window, click, solved[0])
            hints+=1
        lastClick=click
    print 'Hints used:',hints
    print 'Use solve() to check your answers!'

def test():
    print '-solve() solves a puzzle and displays it with the graphics.py module.'
    print '-solveText() solves and displays with text only.'
    print '-hint() is an interactive hint-giver: click an empty space to reveal'
    print '   it! Uses graphics.'
    print '-Use boardFormat() to change an 81-character string into a legal'
    print '   board variable.'
    print
    print '-board1 is a standard board variable.'
    print '-unsolvable is a purposely modified board1 thats unsolvable.'
    print
    print '-On a successful solution, the number of iterations (runs of the main'
    print '   solving function loop, or checks) is displayed.'

if __name__=='__main__':
    test()
    
board1=boardFormat('005204039070030006200800100180009500900600010000050094030400600008007020600023008')
unsolvable=boardFormat('105204039070030006200800100180009500900600010000050094030400600008007020600023008')
