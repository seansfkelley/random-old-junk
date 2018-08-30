#fifteen with graphics
from random import randint
from copy import deepcopy
from graphics import *
from math import sqrt

def convertToRC(window, point, rows, cols):
    row=point.getY()/(window.getWidth()/cols)
    column=point.getX()/(window.getHeight()/rows)
    return [row, column]

def drawGrid(window, rows, cols):
    temp=window.getHeight()/rows
    for i in range(1, rows):
        Line(Point(0, temp), Point(window.getWidth(), temp)).draw(window)
        temp+=(window.getHeight()/rows)
    temp=window.getWidth()/cols
    for i in range(1, cols):
        Line(Point(temp, 0), Point(temp, window.getHeight())).draw(window)
        temp+=(window.getWidth()/cols)

def makeBoard(sides, window, load=False):
    if load:
        temp=open('fifteen.txt', 'r')
        temp=temp.readlines()[0]
        out=[]
        count=0
        while count<len(temp):
            if temp[count] in '1234567890*':
                if temp[count]=='*':
                    out+=['*']
                    count+=1
                    continue
                if temp[count+1] in '1234567890':
                    out+=[int(temp[count]+temp[count+1])]
                    count+=2
                else:
                    out+=[int(temp[count])]
            count+=1
        count=0
        temp=[]
        out2=[]
        while count<len(out):
            temp+=[out[count]]
            if (count+1)%sqrt(len(out))==0:
                out2+=[temp]
                temp=[]
            count+=1
        out=out2
        print 'Loaded'
    else:
        out=[]
        count=1
        for i in range(1, sides+1):
            temp=[]
            for j in range(1, sides+1):
                temp+=[count]
                count+=1
            out+=[temp]
        out[-1][-1]='*'
    texts=[]
    for i in range(sides**2):
        texts+=[Text(Point(0,0), str(i+1))]
        texts[-1].setSize(16)
    texts[-1].setText('*')
    drawBoard(out, window, texts)
    return [out, texts]

def drawBoard(board, window, texts):
    for i in texts:
        i.move((i.getAnchor().getX())*-1, (i.getAnchor().getY())*-1)
        i.undraw()
    count=0
    while count<len(board):
        scount=0
        while scount<len(board[count]):
            bcs=board[count][scount]
            if bcs=='*': bcs=len(board)**2
            temp=window.getHeight()/(len(board)*2)
            texts[bcs-1].move(temp, temp)
            texts[bcs-1].move(temp*2*count, temp*2*scount)
            texts[bcs-1].draw(window)
            scount+=1
        count+=1

def findBlank(board):
    for i in range(0, len(board)):
        for j in range(0, len(board)):
            if board[i][j]=='*':
                return [i,j]

def findNum(board, num):
    for i in range(0, len(board)):
        for j in range(0, len(board)):
            if board[i][j]==num:
                return [i,j]
    return [-1,-1]

def inRange(board, location):
    return location[0]>=0 and location[0]<len(board)\
           and location[1]>=0 and location[1]<len(board)

def numsAdjToBlank(board):
    blankLoc=findBlank(board)
    north=[blankLoc[0]-1, blankLoc[1]]
    east=[blankLoc[0], blankLoc[1]+1]
    south=[blankLoc[0]+1, blankLoc[1]]
    west=[blankLoc[0], blankLoc[1]-1]
    out=[]
    if inRange(board, north):
        out+=[board[north[0]][north[1]]]
    if inRange(board, east):
        out+=[board[east[0]][east[1]]]
    if inRange(board, south):
        out+=[board[south[0]][south[1]]]
    if inRange(board, west):
        out+=[board[west[0]][west[1]]]
    return out

def isAdjToBlank(board, num):
    return num in numsAdjToBlank(board)

def makeMove(board, num):
    boardCopy=deepcopy(board)
    if isAdjToBlank(boardCopy, num):
        blankLoc=findBlank(board)
        numLoc=findNum(boardCopy, num)
        boardCopy[blankLoc[0]][blankLoc[1]]=num
        boardCopy[numLoc[0]][numLoc[1]]='*'
    return boardCopy

def shuffle(board, amount):
    boardCopy=deepcopy(board)
    for i in range(amount):
        temp=numsAdjToBlank(boardCopy)
        x=randint(0, len(temp)-1)
        boardCopy=makeMove(boardCopy, temp[x])
    return boardCopy

def save(board):
    x=open('fifteen.txt', 'w')
    x.writelines([str(board)])
    print 'Saved'

def askLoad(window):
    q=Text(Point(100, 100), 'Load old game?')
    q.draw(window)
    y=Rectangle(Point(25, 112), Point(75, 137))
    n=Rectangle(Point(125, 112), Point(175, 137))
    y.draw(window)
    n.draw(window)
    yt=Text(Point(50, 125), 'Yes')
    nt=Text(Point(150, 125), 'No')
    yt.draw(window)
    nt.draw(window)
    a=Point(0,0)
    while (a.getY()<112 or a.getY()>137) or\
          ((a.getX()<25 or a.getX()>175) or (125>a.getX()>75)):
        a=window.getMouse()
    if 25<a.getX()<75:
        ret=True
    else:
        ret=False
    q.undraw()
    y.undraw()
    n.undraw()
    yt.undraw()
    nt.undraw()
    return ret

def main(size):
    print 'Fifteen! Click a piece to move it. Triple-click the blank to save.'
    window=GraphWin('Fifteen')
    a=False
    a=askLoad(window)
    drawGrid(window, size, size)
    temp=makeBoard(size, window)
    checker=temp[0]
    texts=temp[1]
    player=makeBoard(size, window, a)[0]
    if not a:
        player=shuffle(player, 1000)
    #print checker
    #print player
    #player is loaded correctly, but drawBoard darws it incorrectly:
            #the rows become the columns and vice versa
    while checker!=player:
        drawBoard(player, window, texts)
        move='*'
        saveTries=-1
        while not isAdjToBlank(player, move) or move=='*':
            if move=='*':
                saveTries+=1
            if saveTries==3:
                saveTries=0
                save(player)
            move=window.getMouse()
            move=convertToRC(window, move, size, size)
            move=player[move[1]][move[0]]
        player=makeMove(player, move)
    print 'Game over.'

main(4)
