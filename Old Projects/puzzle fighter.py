from visual import *
from random import randint
#from operator import indexOf

#constants
NUMPLAYERS=2
BLOCKSIZE=144
ROWS=13
COLS=6
HEIGHT=ROWS*BLOCKSIZE
WIDTH=COLS*BLOCKSIZE
FPS=36
DIAMONDFREQ=25
DROPTIMER=5
SLOWDROP=vector(0,4,0)
FASTDROP=vector(0,48,0)
VERYFASTDROP=vector(0,72,0)
if BLOCKSIZE%VERYFASTDROP[1]!=0:
    raise ValueError
BACKGROUND=(.7,.7,.7)
DIVIDER=(.4,.4,.4)
TIMEDCOLORSHIFT=vector(.4,.4,.4)
COLORDICT={'red':color.red, 'green':color.green, 'yellow':color.yellow, 'blue':color.blue}
COLORS=COLORDICT.keys()
DIAMONDCOLOR=(color.white)
STARTX=3
STARTY=12
CRASHCHANCE=20
SCOREREG=20
SCORETIMED=10
SCORECRASH=30
SCOREDIAMOND=50
TECHBONUS=5000
DIAMONDFACTOR=.5
TIMEDKILLAMOUNT=.5
PAUSEKEY=' '
#area/perimeter for big block scoring?
COMBOFACTOR=1.5
CONTROLS=[['q','e','a','s','d'], ['o','[','l',';','\'']]
SHOWPAIRFROMTL=vector(BLOCKSIZE, -BLOCKSIZE*2.5, .75*BLOCKSIZE)
DROPPATTERNS=['rgbyrg/rgbyrg/rgbyrg/rgbyrg',#ryu
              'yyrrgg/yyrrgg/rrggbb/rrggbb',#chun li
              'gbbbby/grrrry/gbbbby/grrrry',#sakura
              'yyyyyy/bbbbbb/gggggg/rrrrrr',#ken
              'ybggby/ybggby/byrryb/byrryb',#morrigan
              'ggrryy/bggrry/bbggrr/ybbggr',#hsien-ko
              'gggbbb/gggbbb/ryryry/ryryry',#donovan
              'gbbrry/gbbrry/grrbby/grrbby']#felicia

#globals/scene setup
boardNumber=0
pairNumber=2
blockQueue=[]
pause=False
blockNumber=0

scene.center=(0, (BLOCKSIZE*ROWS)/2, 0)

bkrd=box(pos=(0, (BLOCKSIZE*ROWS)/2, -.75*BLOCKSIZE), color=BACKGROUND,
         size=(BLOCKSIZE*(COLS*2+4), BLOCKSIZE*ROWS, BLOCKSIZE/2))
divider=box(pos=(0, (BLOCKSIZE*ROWS)/2, -.25*BLOCKSIZE), color=DIVIDER,
            size=(BLOCKSIZE*4, BLOCKSIZE*ROWS, BLOCKSIZE/2))

scene.userzoom=0
scene.userspin=0
scene.autoscale=0

class OccupiedError(Exception):
    def __init__(self, board, x, y):
        self.board=board
        self.x=x
        self.y=y
    def __str__(self):
        return 'OccupiedError: ('+str(x)+', '+str(y)+') on board '+str(board)

class GameOver(Exception):
    def __init__(self, who):
        self.who=who
    def __str__(self):
        return 'Player '+str(self.who+1)+' eliminated.'

class Board:
    def __init__(self, patternNum):
        global boardNumber
        self.frame=frame()
        self.pattern=DROPPATTERNS[patternNum]
        self.displayPattern()
        self.layout=[[None]*(ROWS+1) for a in range(COLS)]
        self.moving=[]
        self.crashes=[]
        self.timed=[]
        self.control=True
        self.attack=0
        self.enemy=None
        self.dropWaiting=False
        self.counter=0
        self.blockPair=[None]*2
        self.showPair=[sphere(pos=(-1,0,0), radius=.001)]*2
        self.fast=False
        self.diamond=None
        self.decremented=False
        self.dropStatus=0
        self.attackLine=0
        self.score=0
        self.combo=0
        self.killCount=0
        self.tempScore=0
        self.number=boardNumber
        boardNumber+=1
        temp=[self.rotateCCW, self.rotateCW, self.moveLeft, self.toggleFast, self.moveRight]
        self.moves=dict(zip(CONTROLS[self.number], temp))
    def __str__(self):
        return 'Board #'+str(self.number)
    def displayPattern(self):
        sizeOf=BLOCKSIZE/2
        middleOffset=vector(sizeOf/2,sizeOf/2,0)
        leftSide=COLS*BLOCKSIZE/2-sizeOf*len(self.pattern[0])/2.0
        position=vector(0,-BLOCKSIZE,0)
        for line in self.pattern:
            position[0]=leftSide
            for b in line:
                box(pos=position+middleOffset, color=COLORDICT[b],
                    size=[sizeOf]*3, frame=self.frame)
                position[0]+=sizeOf
            position[1]-=sizeOf
    def openSpot(self, coords):
        x,y=coords
        return x>=0 and y>=0 and x<COLS and y<ROWS and self.layout[x][y]==None
    def action(self, which):
        if not which and self.fast:
            self.toggleFast()
        if which:
            if which!=CONTROLS[self.number][3] and self.fast:
                self.toggleFast()
            self.moves[which]()
        if self.control:
            self.controlledStep()
        else:
            self.step()
    def createBigBlocks(self):
        pass
    def rotateCW(self):
        self.rotate(True)
    def rotateCCW(self):
        self.rotate(False)
    def rotate(self, clockwise):
        pivot,other=self.blockPair
        otherPos=[(0,1),(1,0),(0,-1),(-1,0)]
        for i in range(4):
            otherPos[i]=(pivot.x+otherPos[i][0], pivot.y+otherPos[i][1])
        if not clockwise:
            otherPos.reverse()
        for i in range(4):
            if otherPos[i]==(other.x,other.y):
                tryNewOther=otherPos[(i+1)%4]
        if not tryNewOther:
            raise LookupError
        if not self.openSpot(tryNewOther):
            x,y=pivot.x,pivot.y
            if tryNewOther[0]>other.x and self.openSpot([x-1,y]):
                pivot.shift(-1,0)
                other.move(x,y)
            elif tryNewOther[0]<other.x and self.openSpot([x+1,y]):
                pivot.shift(1,0)
                other.move(x,y)
        else:
            other.move(tryNewOther[0],tryNewOther[1])
        self.moving.sort()
    def moveLeft(self):
        self.move(-1)
    def moveRight(self):
        self.move(1)
    def move(self, x):
        x1,y1,x2,y2=self.blockPair[0].x,self.blockPair[0].y,self.blockPair[1].x,self.blockPair[1].y
        #move pivot and other out of the way so they dont stop each other from moving
        self.layout[x1][y1]=self.layout[x2][y2]=None
        legalMove=0<=x1+x<=COLS-1 and not self.layout[x1+x][y1] and\
                   0<=x2+x<=COLS-1 and not self.layout[x2+x][y2]
        #restore pivot and other
        self.layout[x1][y1]=self.blockPair[0]
        self.layout[x2][y2]=self.blockPair[1]
        if legalMove:
            self.blockPair[0].shift(x, 0)
            self.blockPair[1].shift(x, 0)
    def toggleFast(self):
        self.fast=not self.fast
    def controlledStep(self):
        for m in list(self.moving):
            if self.fast:
                m.step(FASTDROP)
            else:
                m.step(SLOWDROP)
        if 0<=len(self.moving)<=1:
            self.control=False
    def step(self, speed=VERYFASTDROP):
        if self.moving:
            for m in list(self.moving):
                m.step(speed)
        else:
            if not self.decremented:
                for t in list(self.timed):
                    t.decrement()
                self.decremented=True
            if self.explode():
                return
            if self.dropStatus==0:#hasnt started
                if self.enemy.attack:
                    self.dropStatus=1
                else:
                    self.dropStatus=2
                self.counter=0
                self.attackLine=len(self.pattern)-1
            #no elif, to catch drops that fail immediately
            if self.dropStatus==2:#finished
                self.turn()
                return
        if self.dropStatus==1:#currently dropping
            self.counter=(self.counter+speed[1])%BLOCKSIZE
            if self.counter==0:
                self.drop()
    def explode(self):
        self.tempScore=0
        self.killCount=0
        self.createBigBlocks()
        if self.diamond:
            self.diamond.diamondSplode()
        attackSize=(COMBOFACTOR**self.combo)*self.killCount*DIAMONDFACTOR
        self.score+=(COMBOFACTOR**self.combo)*self.tempScore*DIAMONDFACTOR
        self.killCount=0
        for c in list(self.crashes):
            c.startReaction()
        attackSize+=(COMBOFACTOR**self.combo)*self.killCount
        self.score+=(COMBOFACTOR**self.combo)*self.tempScore
        success=False
        if attackSize:
            success=True
        if self.enemy.attack:
            temp=self.enemy.attack
            self.enemy.attack-=attackSize
            if self.enemy.attack<0:
                self.enemy.attack=0
            self.enemy.attack=int(self.enemy.attack)
            attackSize-=temp
        if attackSize>0:
            self.attack+=attackSize
        self.attack=int(self.attack)
        self.moving.sort()
        self.combo+=1
        return success
    def turn(self):
        global pairNumber
        self.fast=False
        self.decremented=False
        self.dropStatus=0
        self.combo=0
        newPair=blockQueue[self.number].pop(0)
        if len(blockQueue[self.number])==1:
            t1,t2=None,None
            if pairNumber==DIAMONDFREQ-1:
                t1='diamond'
            elif randint(0,99)<CRASHCHANCE:
                t1='crash'
            if randint(0,99)<CRASHCHANCE:
                t2='crash'
            temp=[[COLORS[randint(0,len(COLORS)-1)], t1]]
            t=COLORS[randint(0,len(COLORS)-1)]
            if t1==t2=='crash':
                while t==temp[0][0]:
                    t=COLORS[randint(0,len(COLORS)-1)]
            temp+=[[t,t2]]
            for i in range(NUMPLAYERS):
                blockQueue[i].append(temp)
            pairNumber=(pairNumber+1)%DIAMONDFREQ
        try:
            self.blockPair[0]=Block(self, STARTX, STARTY, newPair[0][0], 0, newPair[0][1])
        except OccupiedError:
            raise GameOver(self.number)
        self.blockPair[1]=Block(self, STARTX, STARTY+1, newPair[1][0], 0, newPair[1][1])
        self.control=True
        self.moving+=self.blockPair
        self.moving.sort()
        #resort after dropping blockpair
        newPair=blockQueue[self.number][0]
        if NUMPLAYERS==2 and self.number==1:
            temp=vector(SHOWPAIRFROMTL)
            temp[0]=-temp[0]
            otherPosition=vector(0, BLOCKSIZE*ROWS, 0)+temp-vector(0,BLOCKSIZE,0)
        else:
            otherPosition=vector(BLOCKSIZE*COLS, BLOCKSIZE*ROWS, 0)+SHOWPAIRFROMTL-vector(0,BLOCKSIZE,0)
        for i in range(2):
            self.showPair[i].visible=0
            if newPair[i][1]=='crash':
                self.showPair[i]=sphere(pos=otherPosition+vector(0,BLOCKSIZE*i,0),
                                        color=COLORDICT[newPair[i][0]], radius=BLOCKSIZE/2, frame=self.frame)
            elif newPair[i][1]=='diamond':
                self.showPair[i]=box(pos=otherPosition+vector(0,BLOCKSIZE*i,0), axis=(1,1,1),
                                     color=DIAMONDCOLOR, size=[BLOCKSIZE*(5**(1/2))]*3, frame=self.frame)
                self.color='diamond'
            else:
                self.showPair[i]=box(pos=otherPosition+vector(0,BLOCKSIZE*i,0),
                                     color=COLORDICT[newPair[i][0]], size=[BLOCKSIZE]*3, frame=self.frame)
    def drop(self):
        size=self.enemy.attack
        if size>len(self.pattern[0]):
            size=len(self.pattern[0])
        positions=range(len(self.pattern[0]))
        for i in range(size):
            i=positions[randint(0,len(positions)-1)]
            b=Block(self,i,STARTY+1,self.enemy.pattern[self.attackLine][i],DROPTIMER)
            self.moving+=[b]
            positions.remove(i)
        self.enemy.attack-=size
        self.attackLine=(self.attackLine+len(self.pattern)-1)%len(self.pattern)
        if self.enemy.attack==0:
            self.dropStatus=2
        self.moving.sort()

class Block:
    def __init__(self, owner, x, y, color, time=0, kind=None):
        global blockNumber
        if x>=COLS or x<0 or y>=ROWS+1 or y<0:
            raise IndexError
        self.owner=owner
        if self.owner.layout[x][y]:
            raise OccupiedError(owner,x,y)
        owner.layout[x][y]=self
        self.x=x
        self.y=y
        self.color=color
        self.time=time
        self.kind=kind
        self.position=0
        self.number=blockNumber
        blockNumber+=1
        position=vector(x*BLOCKSIZE+BLOCKSIZE/2, y*BLOCKSIZE+BLOCKSIZE/2, 0)
        if kind=='crash':
            self.block=sphere(pos=position, color=COLORDICT[color],
                              radius=BLOCKSIZE/2, frame=owner.frame)
            owner.crashes+=[self]
            self.points=SCORECRASH
        elif kind=='diamond':
            self.block=box(pos=position, color=DIAMONDCOLOR, axis=(1,1,1),#axis?
                           size=[BLOCKSIZE*(5**(1/2))]*3, frame=owner.frame)
            self.owner.diamond=self
            self.points=SCOREDIAMOND
        else:
            self.block=box(pos=position, color=COLORDICT[color],
                           size=[BLOCKSIZE]*3, frame=owner.frame)
            self.points=SCOREREG
            if time:
                self.points=SCORETIMED
                owner.timed+=[self]
                temp=vector(self.block.color)-TIMEDCOLORSHIFT
                for i in range(3):
                    if temp[i]<0:
                        temp[i]=0
                self.block.color=temp
    def __eq__(self, other):
        if not other:
            return False
        return self.number==other.number
    def __ne__(self, other):
        return not self==other
    def __cmp__(self, other):
        if not other:
            return 1
        return self.y-other.y
    def __str__(self):
        return 'Block at ('+str(self.x)+', '+str(self.y)+') on '+str(self.owner)
    def shift(self, x, y):
        #use carefully: does not check legality
        self.owner.layout[self.x][self.y]=None
        self.x+=x
        self.y+=y
        self.owner.layout[self.x][self.y]=self
        self.block.pos+=vector(x*BLOCKSIZE, y*BLOCKSIZE, 0)
        self.position=(self.block.pos[1]-BLOCKSIZE/2)%BLOCKSIZE
    def move(self, x, y):
        self.shift(x-self.x,y-self.y)
    def step(self, speed=SLOWDROP):
        if self.position==0 and (self.owner.layout[self.x][self.y-1] or self.y==0):
            if self in self.owner.blockPair:
                self.owner.blockPair=[None,None]
            self.owner.moving.remove(self)
            return
        self.position=(self.block.pos[1]-BLOCKSIZE/2)%BLOCKSIZE
        if self.position<speed[1] and (self.owner.layout[self.x][self.y-1] or self.y==0):
            self.block.pos[1]-=self.position
        else:
            self.block.pos-=speed
        oldpos=self.position
        self.position=(self.block.pos[1]-BLOCKSIZE/2)%BLOCKSIZE
        if self.position>oldpos:
            self.owner.layout[self.x][self.y]=None
            self.y-=1
            self.owner.layout[self.x][self.y]=self
    def decrement(self):
        if self.time:
            self.time-=1
            if self.time==0:
                self.owner.layout[self.x][self.y]=None
                Block(self.owner, self.x, self.y, self.color)
                self.owner.timed.remove(self)
                self.block.visible=0
    def explodableNeighbors(self):
        exp=[]
        for (i,j) in ((1,0), (0,1), (-1,0), (0,-1)):
            x=self.x+i
            y=self.y+j
            if x>=COLS or x<0 or y>=ROWS or y<0:
                continue
            b=self.owner.layout[x][y]
            if b and (b.color==self.color or b.time):
                exp+=[b]
        return exp
    def startReaction(self):
        if self.kind!='crash':
            return
        e=self.explodableNeighbors()
        for b in list(e):
            if b.time:
                e.remove(b)
        if e:
            self.explode()
    def explode(self):
        self.owner.layout[self.x][self.y]=None
        self.block.visible=0
        self.owner.killCount+=1
        self.owner.tempScore+=self.points
        try: self.owner.moving.remove(self)
        except ValueError: pass
        for b in self.owner.layout[self.x]:
            if b and b.y>self.y and b not in self.owner.moving:
                    self.owner.moving+=[b]
        if self.kind=='diamond':
            return
        elif self.kind=='crash':
            self.owner.crashes.remove(self)
        if self.time:
            self.owner.timed.remove(self)
            self.owner.killCount=self.owner.killCount-1+TIMEDKILLAMOUNT
        else:
            e=self.explodableNeighbors()
            for b in e:
                b.explode()
    def diamondSplode(self):
        self.explode()
        self.owner.diamond=None
        if self.y==0:
            return
        color=self.owner.layout[self.x][self.y-1].color
        for i in self.owner.layout:
            for j in i:
                if j and j.color==color:
                    j.explode()

def parseDropPatterns():
    convert={'r':'red','g':'green','y':'yellow', 'b':'blue'}
    end=[]
    for i in range(len(DROPPATTERNS)):
        key=DROPPATTERNS[i].split('/')
        pattern=[]
        for line in key:
            temp=[]
            for letter in line:
                temp+=[convert[letter]]
            pattern+=[temp]
        end+=[pattern]
    return end

if __name__=='__main__':
    print 'TO DO:'
    print 'glowing blocks?'
    print 'block settling - should it have to stick on whatever its on for a couple frames before being final?'
    print 'implement combos/large blocks/different ratios of effectiveness for breaks'
    print 'show score/attack size to players'
    print 'check the disallow-two-crashes-of-same-color code'
    print 'fix down-toggling'
    for i in range(2):
        blockQueue+=[[]]
        for j in range(2):
        #double loops: too lazy to copy paste and change
            t=None
            if randint(0,99)<CRASHCHANCE:
                t='crash'
            blockQueue[-1]+=[[COLORS[randint(0, len(COLORS)-1)], t]]
    blockQueue=[blockQueue,list(blockQueue)]
    DROPPATTERNS=parseDropPatterns()
    one=Board(randint(0,len(DROPPATTERNS)-1))
    two=Board(randint(0,len(DROPPATTERNS)-1))
    one.enemy=two
    two.enemy=one
    one.frame.pos=(-BLOCKSIZE*(COLS+2), 0, 0)
    two.frame.pos=(BLOCKSIZE*2, 0, 0)
    kb=scene.kb
    one.turn()
    two.turn()
    while True:
        rate(FPS)
        oneKey=twoKey=None
        while kb.keys:
            key=kb.getkey()
            if key==PAUSEKEY:
                pause=not pause
                continue
            if one.control and oneKey==None and key in CONTROLS[0]:
                if key==CONTROLS[0][3] and one.fast:
                    continue
                oneKey=key
            elif two.control and twoKey==None and key in CONTROLS[1]:
                if key==CONTROLS[1][3] and two.fast:
                    continue
                twoKey=key
        if pause:
            continue
        try:
            print oneKey
            one.action(oneKey)
            two.action(twoKey)
        except GameOver, g:
            print g
            break
