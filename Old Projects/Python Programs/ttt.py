#Tic Tac Toe

on=True
turn=9
char=""
move=""

def play(char, move):
    x=10
    while x>9 or x<1 or move[x-1]=="X" or move[x-1]=="O":
        x=input(char+": enter move: ")
    move=move[0:x-1]+char+move[x:]
    line1=move[0] + "|" + move[1] + "|" + move[2]
    line2=move[3] + "|" + move[4] + "|" + move[5]
    line3=move[6] + "|" + move[7] + "|" + move[8]
    print
    print line1
    print line2
    print line3
    return move

def changeturn(char):
    if char=="X":
        char="O"
    else:
        char="X"
    return char


def check(turn):
    if move[0]==move[1] and move[1]==move[2]:
        print "Tic-Tac-Toe! " + move[0] + " wins!"
        turn=9
    if move[3]==move[4] and move[4]==move[5]:
        print "Tic-Tac-Toe! " + move[3] + " wins!"
        turn=9
    if move[6]==move[7] and move[7]==move[8]:
        print "Tic-Tac-Toe! " + move[6] + " wins!"
        turn=9
    if move[0]==move[3] and move[3]==move[6]:
        print "Tic-Tac-Toe! " + move[0] + " wins!"
        turn=9
    if move[1]==move[4] and move[4]==move[7]:
        print "Tic-Tac-Toe! " + move[1] + " wins!"
        turn=9
    if move[2]==move[5] and move[5]==move[8]:
        print "Tic-Tac-Toe! " + move[2] + " wins!"
        turn=9
    if move[0]==move[4] and move[4]==move[8]:
        print "Tic-Tac-Toe! " + move[0] + " wins!"
        turn=9
    if move[2]==move[4] and move[4]==move[6]:
        print "Tic-Tac-Toe! " + move[2] + " wins!"
        turn=9
    return turn
    
while on==True:
    if turn==9:
        char="X"
        move="123456789"
        turn=0
        print
        print "1|2|3"
        print "4|5|6"
        print "7|8|9"
    turn+=1
    move=play(char, move)
    turn=check(turn)
    char=changeturn(char)

