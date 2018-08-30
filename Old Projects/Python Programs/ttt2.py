#tictactoe

def makeboard(size):
    board=[]
    currow=[]
    for i in range(1,size**2+1):
        currow+=[i]
        if i%size==0:
            board=board+[currow]
            currow=[]
    return board

def printboard(board):
    count=0
    row=1
    while count<len(board[0]):
        print "  "+str(count+1),
        count+=1
    count=0
    line=[""]*int(len(board)+1)
    print
    for i in board:
        print str(row),
        while count<len(i)-1:
            if str(i[count]) not in str(range(1, (len(board)**2)+1)):
                line[row]+=str(i[count])+" | "
            else:
                line[row]+="  | "
            count+=1
        if count<len(i):
            if str(i[count]) not in str(range(1, (len(board)**2+1))):
                line[row]+=str(i[count])
            else:
                line[row]+=" "
            count+=1
        print line[row]
        if row<len(board):
            print " "+"---|"*(len(line)-2)+"---"
        row+=1
        count=0
        
def makemove(player,board):
    print
    retry=True
    print "It is "+player+"'s turn."
    while retry==True:
        r=input("Enter the row: ")
        c=input("Enter the column: ")
        if r<=len(board) and c<=len(board) and str(board[r-1][c-1]) not in "XO":
            print
            board[r-1][c-1]=player
            retry=False
        else:
            print "Invalid location. Pick another."
    return board

def checkrows(board):
    winner=" "
    count=0
    while count<len(board[0]):
        match=True
        scount=0
        while match==True and scount<(len(board)-1):
            if board[count][scount]!=board[count][scount+1]:
                match=False
            scount+=1
        if match==True:
            winner=str(board[count][0])
        count+=1
    return winner

def checkcolumns(board):
    winner=" "
    count=0
    while count<len(board):
        match=True
        scount=0
        while match==True and scount<(len(board)-1):
            if board[scount][count]!=board[scount+1][count]:
                match=False
            scount+=1
        if match==True:
            winner=str(board[0][count])
        count+=1
    return winner

def checkdiagonals(board):
    winner=" "
    count=0
    match=True
    while match==True and count<(len(board)-1):
        if board[count][count]!=board[count+1][count+1]:
            match=False
        count+=1
    if match==True:
        winner=str(board[count][count])
    count=0
    if match==False:
        scount=len(board)-1
        match=True
        while match==True and scount>-1 and count<len(board)-1:
            if board[count][scount]!=board[count+1][scount-1]:
                match=False
            scount-=1
            count+=1
        if match==True:
            winner=str(board[0][len(board)-1])
    return winner

def determinewinner(board):
    winner=" "
    winner=checkrows(board)
    winner=checkcolumns(board)
    winner=checkdiagonals(board)
    return winner

def tictactoe(size):
    board=makeboard(size)
    winner=" "
    movesmade=0
    printboard(board)
    while movesmade<size**2:
        board=makemove('X',board)
        printboard(board)
        if determinewinner(board)!=" ":
            break
        movesmade+=1
        if movesmade==size**2:
            break
        board=makemove('O',board)
        printboard(board)
        if determinewinner(board)!=" ":
            break
        movesmade+=1
        if movesmade==size**2:
            break
    if determinewinner(board)==" ":
        print
        print "Tie!"
    else:
        print
        print determinewinner(board), "wins!"
