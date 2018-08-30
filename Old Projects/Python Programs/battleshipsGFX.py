from graphics import *

class Ship:
    def __init__(self, name):
        self.__name=name
        self.__locs=[]
        self.__hits=[]
        self.__rects=[]
    def __str__(self):
        return self.__name+':\nHits: '+str(len(self.__hits))+'/'+str(len(self.__locs))
    def getLocs(self):
        return self.__locs
    def addLoc(self, loc):
        self.__locs+=[loc]
    def getName(self):
        return self.__name
    def isAlive(self):
        return len(self.__locs)!=len(self.__hits)
    def addHit(self, loc):
        self.__hits+=[loc]

class Player:
    def __init__(self, name, ships=[]):
        self.__ships=ships
        self.__name=name
        self.__numShips=len(ships)
        self.__attacks=[]
    def removeShip(self, shipName):
        for i in self.__ships:
            if i.getName()==shipName:
                self.__ships.remove(i)
                self.__numShips-=1
                break
    def addNewShip(self, shipName, locs):
        self.__ships+=[Ship(shipName, locs)]
        self.__numShips+=1
    def addOldShip(self, ship):
        self.__ships+=[ship]
        self.__numShips+=1
    def getShips(self):
        return self.__ships
    def addAttack(self, loc):
        self.__attacks+=[loc]
    def getAttacks(self):
        return self.__attacks
    def getAttWin(self):
        return self.__attackWin
    def getShipWin(self):
        return self.__shipWin
    def setAttWin(self, window):
        self.__attackWin=window
    def setShipWin(self, window):
        self.__shipWin=window

def drawRect(coord, color, window):
    side=window.getWidth()
    a=Point(40*coord[1], 40*coord[0])
    b=Point(40*coord[1]+40, 40*coord[0]+40)
    rect=Rectangle(a,b)
    rect.setFill(color)
    rect.draw(window)
##    return rect

def drawCir(coord, color, window):
    side=window.getWidth()
    center=Point(40*coord[1]+20, 40*coord[0]+20)
    cir=Circle(center, 7)
    cir.setFill(color)
    cir.draw(window)
##    return cir
    
def convertToRC(window, point): 
    row=point.getY()/(window.getWidth()/10)
    col=point.getX()/(window.getHeight()/10)
    return [row, col]

def drawGrid(window):
    temp=window.getHeight()/10
    for i in range(1, 10):
        Line(Point(0, temp), Point(window.getWidth(), temp)).draw(window)
        temp+=(window.getHeight()/10)
    temp=window.getWidth()/10
    for i in range(1, 10):
        Line(Point(temp, 0), Point(temp, window.getHeight())).draw(window)
        temp+=(window.getWidth()/10)

def available(shipList, coord):
    """Checks if the space is occupied by a ship."""
    for i in shipList:
        for j in i.getLocs():
            if j==coord:
                return False
    return True

def allAdj(ship):
    """Returns all adjacent spaces to a ship. Removes diagonals and points
    on the ship itself."""
    locs=ship.getLocs()
    spaces=[]
    for i in locs:
        spaces+=findAdj(i)
    temp=0
    while temp<len(spaces):
        if spaces[temp] in locs or not available([ship], spaces[temp]):
            spaces=spaces[:temp]+spaces[temp+1:]
            continue
        temp+=1
    return spaces

def findAdj(coord):
    """Finds the north, south, east, and west adjacent points. Removes points
    off the board."""
    y=coord[0]
    x=coord[1]
    ret=[[y-1,x],[y,x+1],[y+1,x],[y,x-1]]
    temp=0
    while temp<len(ret):
        if (not -1<ret[temp][0]<10) or (not -1<ret[temp][1]<10):
            ret=ret[:temp]+ret[temp+1:]
            continue
        temp+=1
    return ret

def isAdj(ship, coord):
    """Boolean to check if a point is adjacent to a ship."""
    if len(ship.getLocs())==0:
        return True
    return coord in allAdj(ship)

def inLine(ship, coord):
    """Boolean checking if a poitn is in line with the rest of the ship."""
    if len(ship.getLocs())==0:
        return True
    if len(ship.getLocs())==1 and isAdj(ship, coord):
        return True
    if ship.getLocs()[0][0]==ship.getLocs()[1][0]:
        if coord[0]==ship.getLocs()[0][0]:
            return True
    else:
        if coord[1]==ship.getLocs()[0][1]:
            return True
    return False

def addShip(player, shipName, shipLength, shipWin):
    """User mouse input fuction for adding a ship."""
    print 'Place coordinates of '+shipName+' ('+str(shipLength)+').'
    ship=Ship(shipName)
    legalMoves=0
    while legalMoves<shipLength:
        curCoord=shipWin.getMouse()
        temp=convertToRC(shipWin, curCoord)
        if (not available(player.getShips(), temp)) or (not isAdj(ship, temp))\
           or (not inLine(ship, temp)) or (temp[0]==10 or temp[1]==10):
            print 'Illegal choice.'
            continue
        legalMoves+=1
        drawRect(temp, color_rgb(150, 150, 150), shipWin)
        ship.addLoc(temp)
    player.addOldShip(ship)

def setup(player):
    """Standard game setup, 5 ships."""
    shipWin=GraphWin('Your Fleet', 400, 400)
    player.setShipWin(shipWin)
    drawGrid(shipWin)
    addShip(player, 'Patrol Boat', 2, shipWin)
    addShip(player, 'Destroyer', 3, shipWin)
    addShip(player, 'Submarine', 3, shipWin)
    addShip(player, 'Battleship', 4, shipWin)
    addShip(player, 'Aircraft Carrier', 5, shipWin)
    attackWin=GraphWin('Attacks', 400, 400)
    drawGrid(attackWin)
    player.setAttWin(attackWin)

def setupComp(player):
    return

def attack(attacked, attacker, coord):
    """Attack a player. Text and color change response."""
    attackWin=attacker.getAttWin()
    shipWin=attacked.getShipWin()
    attacker.addAttack(coord)
    for i in attacked.getShips():
        for j in i.getLocs():
            if j==coord:
                i.addHit(coord)
                print 'Hit!'
                drawCir(coord, color_rgb(200, 100, 100), shipWin)
                drawCir(coord, color_rgb(200, 100, 100), attackWin)
                if not i.isAlive():
                    print 'You sunk a '+i.getName()+'!'
                return
    print 'Miss!'
    drawCir(coord, 'white', attackWin)
    drawCir(coord, 'white', shipWin)

def lose(player):
    """Checks all of a player's ships to see if they are alive."""
    for i in player.getShips():
        if i.isAlive:
            return False
    return True

def game(player1, player2):
    setup(player1)
    setup(player2)
    tempNum=0
    players=[player1, player2]
    while not lose(player1) and not lose(player2):
        attWin=players[tempNum].getAttWin()
        coord=attWin.getMouse()
        coord=convertToRC(attWin, Point(int(coord.getX()), int(coord.getY())))
        if coord[0]==10 or coord[1]==10 or coord in \
           players[tempNum].getAttacks():
            print 'Illegal choice.'
            continue
        attack(players[1-tempNum], players[tempNum], coord)
        tempNum=1-tempNum
    print players[1-tempNum].getName()+' wins!'
        
human1=Player('Player1')
human2=Player('Player2')
game(human1, human2)
