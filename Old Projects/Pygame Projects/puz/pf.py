#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

import pygame, os, sys
from pygame.locals import *
from random import randint

#board constants
BD_H,BD_W=13,6 #spaces
START_COL,START_ROW=3,0 #initial block pair location

#block constants
COLORS=('red', 'green', 'blue', 'yellow')
BK_SIZE=32 #px
DIAMOND_FREQ=25
CRASH_CHANCE=20 #%
EXPLODE_DELAY=3 #frames before spreading explosion
EXPLODE_TIME=20 #frames before removing exploding block

#play constants
SPEED=2 #px/fr
FAST_SPEED=8
VERY_FAST_SPEED=16

#window constants
W_TOP,W_BOT,W_SIDE,W_MID=64,128,64,128
W_H=W_TOP+W_BOT+BD_H*BK_SIZE
W_W=2*W_SIDE+W_MID+2*BD_W*BK_SIZE

#other constants
FRAMERATE=30

#globals after class declarations

if BK_SIZE%SPEED!=0 or BK_SIZE%FAST_SPEED!=0 or BK_SIZE%VERY_FAST_SPEED:
    raise ValueError('invalid values for fall speed constants')

class XYVector:
    'Barebones, 2D vector class.'
    def __init__(self, xy_or_x, y=None):
        if y is None:
            self.x,self.y=xy_or_x
        else:
            self.x=xy_or_x
            self.y=y
    def __add__(self, other):
        return XYVector(self.x+other.x, self.y+other.y)
    def __sub__(self, other):
        return XYVector(self.x-other.x, self.y-other.y)
    def __mul__(self, scalar):
        #doesn't work as int*vector...
        return XYVector(self.x*scalar, self.y*scalar)
    def __neg__(self):
        return XYVector(-self.x, -self.y)
    def __eq__(self, other):
        return self.x==other.x and self.y==other.y
    def __getitem__(self, which):
        if which==0:
            return self.x
        elif which==1:
            return self.y
        raise IndexError
    def __setitem__(self, key, value):
        if key==0:
            self.x=value
        elif key==1:
            self.y=value
        raise IndexError
    def __str__(self):
        return 'Vector<%f, %f>' % (self.x, self.y)

class Block(pygame.sprite.Sprite):
    def __init__(self, board, pos, color):
        pygame.sprite.Sprite.__init__(self)
        self.board=board
        self.color=color
        self.landed=False
        self.pos=XYVector(pos)
        self.explode_life=0
        board.blocks[pos[0]][pos[1]]=self
        board.add(self)
    def update(self):
        'Moves block appropriately and returns if there is more to move.'
        if self.explode_life:
            self.explode()
            return False
        if self.landed:
            return False
        delta=self.board.coords.y+self.pos.y*BK_SIZE-self.rect.topleft[1]
        if delta:
            screen.blit(blank_block, self.rect.topleft)
            if delta%self.board.speed:
                delta%=self.board.speed
            else:
                delta=self.board.speed
            self.rect.center=(self.rect.center[0],
                              self.rect.center[1]+delta)
        elif self.board.is_open(self.pos.x, self.pos.y+1):
            screen.blit(blank_block, self.rect.topleft)
            self.board.blocks[self.pos.x][self.pos.y]=None
            self.board.blocks[self.pos.x][self.pos.y+1]=self
            self.rect.center=(self.rect.center[0],
                              self.rect.center[1]+self.board.speed)
            self.pos.y+=1
        else:
            self.landed=True
            return False
        return True
    def neighbors(self):
        'Returns a list of this blocks 4 neighboring spaces.'
        n=[]
        for x, y in ((0,1), (1,0), (0,-1), (-1,0)):
            try: 
                if self.board.blocks[self.pos.x+x][self.pos.y+y]:
                    n.append(self.board.blocks[self.pos.x+x][self.pos.y+y])
            except IndexError:
                pass
        return n
    def move(self, delta):
        'Moves block to a new relative position, removes old position.'
        self.board.blocks[self.pos.x][self.pos.y]=None
        screen.blit(blank_block, self.rect.topleft)
        self.pos=self.pos+delta
        self.board.blocks[self.pos.x][self.pos.y]=self
        self.rect.center=tuple(delta*BK_SIZE+XYVector(self.rect.center))
    def explode(self, initial=False):
        if self.explode_life==0:
            self.board.exploders.append(self)
        self.explode_life+=1
        if self.explode_life==EXPLODE_DELAY or initial:
            self.explode_life=EXPLODE_DELAY
            neigh=self.neighbors()
            for n in neigh:
                if n.explode_life==0 and n.color==self.color:
                    n.explode()
        elif self.explode_life==EXPLODE_TIME:
            screen.blit(blank_block, self.rect.topleft)
            self.board.blocks[self.pos.x][self.pos.y]=None
            self.kill()
            self.board.exploders.remove(self)
            return
        #change image?
                          
class Gem(Block):
    def __init__(self, board, pos, color, time=None):
        Block.__init__(self, board, pos, color)
        self.image,self.rect=image_dict['Gem-%s-small' % color]
        self.rect=self.rect.copy()
        self.rect.topleft=tuple(self.pos*BK_SIZE+board.coords)
        
class Crash_Gem(Block):
    def __init__(self, board, pos, color, time=None):
        Block.__init__(self, board, pos, color)
        self.image,self.rect=image_dict['CrashGem-%s' % color]
        self.rect=self.rect.copy()
        self.rect.topleft=tuple(self.pos*BK_SIZE+board.coords)
        board.crash_gems.append(self)
    def init_explode(self):
        if self.explode_life:
            return
        for n in self.neighbors():
            if n.color==self.color and not isinstance(n, Counter_Gem):
                self.explode(True)
        
class Counter_Gem(Block):
    def __init__(self, board, pos, color, time):
        Block.__init__(self, board, pos, color)
        self.image,self.rect=image_dict['CounterGem-%s-%d' % (color, time)]
        self.rect=pygame.Rect(self.rect)
        self.rect.topleft=tuple(self.pos*BK_SIZE+board.coords)
        self.time=time
        self.new=True
        board.counter_gems.append(self)
    def decrement(self):
        'Lowers timer, replaces with regular Gem is appropriate.'
        if self.new:
            self.new=False
            return
        self.time-=1
        if self.time==0:
            screen.blit(blank_block, self.rect.topleft)
            self.board.blocks[self.pos.x][self.pos.y]=Gem(self.board, self.pos, self.color)
            self.kill()
            self.board.counter_gems.remove(self)
        else:
            self.image=image_dict['CounterGem-%s-%d' % (self.color, self.time)][0]
    def update(self):
        return Block.update(self)

class Diamond:
    def __init__(self, board, pos):
        pass
        
class Block_Pair:
    def __init__(self, board):
        self.board=board
        if randint(0,99)<=CRASH_CHANCE:
            self.pivot=Crash_Gem(board, (START_COL, START_ROW+1), COLORS[randint(0,3)])
        else:
            self.pivot=Gem(board, (START_COL, START_ROW+1), COLORS[randint(0,3)])
        if diamond_count==0:
            self.other=Diamond(board, (START_COL, START_ROW))
        elif randint(0,99)<=CRASH_CHANCE:
            self.other=Crash_Gem(board, (START_COL, START_ROW), COLORS[randint(0,3)])
        else:
            self.other=Gem(board, (START_COL, START_ROW), COLORS[randint(0,3)])
    def update(self):
        'Moves blocks, returns False if _either_ block has landed.'
        more_to_move=True
        #cant compress with OR, short circuiting would mess it up
        if self.pivot.pos.y>self.other.pos.y:
            if not self.pivot.update():
                more_to_move=False
            if not self.other.update():
                more_to_move=False
        else:
            if not self.other.update():
                more_to_move=False
            if not self.pivot.update():
                more_to_move=False
        return more_to_move
    def move(self, left=True):
        'Moves the blocks left or right, if possible.'
        if left:
            v=XYVector(-1,0)
        else:
            v=XYVector(1,0)
        if self.pivot.pos.y==self.other.pos.y:
            if left:
                if self.pivot.pos.x>self.other.pos.x:
                    outer=self.other
                else:
                    outer=self.pivot
            else:
                if self.pivot.pos.x<self.other.pos.x:
                    outer=self.other
                else:
                    outer=self.pivot
            if self.board.is_open(outer.pos+v):
                outer.move(v)
                if outer is self.pivot:
                    self.other.move(v)
                else:
                    self.pivot.move(v)
        elif self.board.is_open(self.pivot.pos+v) and self.board.is_open(self.other.pos+v):
            self.pivot.move(v)
            self.other.move(v)
    def rotate(self, cw):
        'Rotates other around pivot, if possible.'
        if self.other.pos.y>self.pivot.pos.y:
            index=0
        elif self.other.pos.y<self.pivot.pos.y:
            index=2
        elif self.other.pos.x>self.pivot.pos.x:
            index=1
        else:
            index=3
        if cw:
            index=(index+3)%4
            rot=-rotations[index]
        else:
            rot=rotations[index]
        if not self.board.is_open(self.other.pos+rot):
            if self.other.pos.y!=self.pivot.pos.y:
                #second check to keep players from infintely hovering
                if not self.board.is_open(self.pivot.pos+XYVector(-rot.x, 0)):
                    #no room to move the pivot away, so switch
                    self.pivot.move(XYVector(0, -rot.y))
                    self.other.move(XYVector(0, rot.y))
                    #undo the deletion from moving other
                    self.board.blocks[self.pivot.pos.x][self.pivot.pos.y]=self.pivot
                else:
                    #shove pivot out of the way
                    self.pivot.move(XYVector(-rot.x, 0))
                    self.other.move(XYVector(0, rot.y))
        else:
            self.other.move(rot)

class Board(pygame.sprite.Group):
    def __init__(self, x, y):
        pygame.sprite.Group.__init__(self)
        self.blocks=[[None]*BD_H for i in xrange(BD_W)]
        self.coords=XYVector(x, y)
        self.counter_gems=[]
        self.crash_gems=[]
        self.exploders=[]
        self.current_pair=None
        self.speed=SPEED
        self.decremented=False
        self.down=False
        self.enemy=None
    def is_open(self, x, y=None):
        if y==None:
            x,y=x
        if x<0 or y<0:
            return False
        try:
            return self.blocks[x][y]==None
        except IndexError:
            return False
    def update(self):
        all_fallen=True
        if self.current_pair==None:
            for y in xrange(1, BD_H+1):
                y=BD_H-y
                for x in xrange(BD_W):
                    if self.blocks[x][y] and self.blocks[x][y].update():
                        all_fallen=False
        else:
            all_fallen=False
            if not self.current_pair.update():
                self.current_pair=None
                self.speed=VERY_FAST_SPEED
        if all_fallen:
            if not self.decremented:
                for c in tuple(self.counter_gems):
                    c.decrement()
            if self.explode():
                self.next_turn()
    def left(self):
        if self.current_pair:
            self.current_pair.move(True)
    def right(self):
        if self.current_pair:
            self.current_pair.move(False)
    def rotate_CW(self):
        if self.current_pair:
            self.current_pair.rotate(True)
    def rotate_CCW(self):
        if self.current_pair:
            self.current_pair.rotate(False)
    def fast_drop_on(self):
        self.down=True
        if self.current_pair:
            self.speed=FAST_SPEED
    def fast_drop_off(self):
        self.down=False
        if self.current_pair:
            self.speed=SPEED
    def explode(self):
        'Explodes appropriate blocks, returns True if the turn is over.'
        if self.exploders:
            return False
        for c in tuple(self.crash_gems):
            c.init_explode()
        if not self.exploders:
            falling_cols=range(BD_W)
            still_to_drop=True
            for y in xrange(1, BD_H+1):
                y=BD_H-y
                for x in tuple(falling_cols):
                    if self.blocks[x][y]==None:
                        for y2 in xrange(y):
                            if self.blocks[x][y2]:
                                still_to_drop=False
                                self.blocks[x][y2].landed=False
                        falling_cols.remove(x)
            return still_to_drop
        return False
    def next_turn(self):
        self.current_pair=Block_Pair(self)
        self.decremented=False
        if self.down:
            self.speed=FAST_SPEED
        else:
            self.speed=SPEED

#globals
diamond_count=1
pair_queue=[]
rotations=[XYVector(1,-1), XYVector(-1,-1), XYVector(-1,1), XYVector(1,1)]
      #CW  top>right       right->bottom    bottom>left     left>top
block_queue=[]

def handle_input(events):
    for event in events:
        if event.type==QUIT:
            sys.exit(0)
        elif event.type==KEYDOWN:
            try:
                down_controls[event.key]()
            except KeyError:
                pass
        elif event.type==KEYUP:
            try:
                up_controls[event.key]()
            except KeyError:
                pass

def load_image(name, color_key=None, scaling=1):
    pathname=os.path.join('data',name)
    try:
        image=pygame.image.load(open(pathname))
    except pygame.error, msg:
        raise SystemExit, msg
    image=image.convert()
    if color_key:
        if color_key==-1:
            color_key=image.get_at((0,0))
        image.set_colorkey(color_key, RLEACCEL)
    if scaling!=1:
        image=scale(image, (int(image.get_size()[0]*scaling),
                            int(image.get_size()[1]*scaling)))
    return (image, image.get_rect())

def run_game():
    clock=pygame.time.Clock()
    
    while True:
        clock.tick(FRAMERATE)
        handle_input(pygame.event.get())
        p1.update()
        p1.draw(screen)
        #p2.update()
        #p2.draw(screen)
        pygame.display.flip()

if __name__=='__main__':
    pygame.init()

    if not pygame.font.get_init():
        raise SystemExit

    window=pygame.display.set_mode((W_W,W_H))
    pygame.display.set_caption('Super Puzzle Fighter II Turbo')
    screen=pygame.display.get_surface()
    
    blank_block=pygame.Surface((BK_SIZE, BK_SIZE))
    blank_block=blank_block.convert()
    blank_block.fill((0,0,0))

    image_dict={}
    for color in COLORS:
        for size in ['small', 'large']:
            name='Gem-%s-%s' % (color, size)
            image_dict[name]=load_image(name+'.png', -1)
        for i in xrange(1,6):
            name='CounterGem-%s-%d' % (color, i)
            image_dict[name]=load_image(name+'.gif', -1)
        name='CrashGem-%s' % color
        image_dict[name]=load_image(name+'.gif', -1)

    p1=Board(W_SIDE, W_TOP)
    p2=Board(W_SIDE+W_MID+BD_W*BK_SIZE, W_TOP)
    p1.enemy=p2
    p2.enemy=p1
    
    down_controls={K_q:p1.rotate_CCW,
                   K_a:p1.left,
                   K_s:p1.fast_drop_on,
                   K_d:p1.right,
                   K_e:p1.rotate_CW,
                   K_o:p2.rotate_CCW,
                   K_l:p2.left,
                   K_SEMICOLON:p2.fast_drop_on,
                   K_QUOTE:p2.right,
                   K_LEFTBRACKET:p2.rotate_CW}
    up_controls={K_s:p1.fast_drop_off,
                 K_SEMICOLON:p2.fast_drop_off}
                 

    #scale=pygame.transform.smoothscale
    #rotate=pygame.transform.rotate

    print 'To be fixed:'
    print 'blocks move into new position when they are fully lined up with it'
    print '    not when the just enter into it'

    run_game()
