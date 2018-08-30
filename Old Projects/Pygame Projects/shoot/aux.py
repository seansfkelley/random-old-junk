import pygame, sys, os
from pygame.locals import *
from random import random

#----------------------------------------------------------------------CONSTANTS

#------------------------------------------------------------------------visuals
XRES,YRES=600,800
DIS_FLAGS=0
IMG_NAMES=['ship', 'shot', 'enemy', 'life']
SHOT_NAME_DEF='shot'

IMG_COLORKEY_DEF=(216,106,47)
IMG_SCALE_DEF=.5

LIFE_IMG_OFFSET=(30,30)
LIFE_SPACING=4

ALPHA_THRESHOLD=10

#--------------------------------------------------------------internal settings
VERT_BUFFER=100
PLAY_AREA=pygame.Rect(0,-VERT_BUFFER,XRES,YRES+VERT_BUFFER)
VISIBLE_AREA=pygame.Rect(0, 0, XRES, YRES)
FRAMERATE=30
IMG_EXT='.png'
IMG_DIR='images'

#-----------------------------------------------------------------------gameplay
MOVE_SPEED_VERT,MOVE_SPEED_HORIZ=10,8

P1_CONTROLS=(K_w,K_s,K_a,K_d,K_LCTRL)
P2_CONTROLS=(K_UP,K_DOWN,K_LEFT,K_RIGHT,K_SPACE)
P1_START_POS=(XRES/3,YRES-100)
P2_START_POS=(2*XRES/3,YRES-100)
P1_START_BUTTON=K_6
P2_START_BUTTON=K_7

RESPAWN_TIME=FRAMERATE*1.5

SHOT_SPD_Y_DEF=30
SHOT_INT_DEF=8 #frames

DMG_DEF=1
DMG_COLLIDE=2

NUM_LEVELS=1
NUM_LIVES=3

ENEMY_LIFE=2
ENEMY_MAX_Y_DEF=YRES-150

#---------------------------------------------------------------------------misc
NAME='Vertical Shooter!'

#------------------------------------------------------------------------aliases
scale=pygame.transform.smoothscale
rotate=pygame.transform.rotate

#------------------------------------------------------------------------globals
images={}
ship_group=pygame.sprite.Group()
shot_group=pygame.sprite.Group()
enemy_group_collidable=pygame.sprite.Group()
enemy_group_all=pygame.sprite.Group()
enemy_shot_group=pygame.sprite.Group()
life_group=pygame.sprite.Group()

#------------------------------------------------------------------------CLASSES

class Vector:
    def __init__(self, xy_or_x, y=None):
        if y is None:
            self.x,self.y=xy_or_x
        else:
            self.x=xy_or_x
            self.y=y
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)
    def __mul__(self, scalar):
        #doesn't work as int*vector...
        return Vector(self.x*scalar, self.y*scalar)
    def __neg__(self):
        return Vector(-self.x, -self.y)
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
    def to_tuple(self):
        return (self.x, self.y)

class DummyShip:
    def __init__(self, controls):
        self.controls=controls
    def keydown(self, key):
        return key in self.controls
    def keyup(self, key):
        return key in self.controls

class SwarmGen:
    def __init__(self, specs, num=1, interval=0):
        self.specs=specs
        self.num=num
        self.interval=interval
    def generate(self, level, offset=0, num=None, interval=None):
        if num is None:
            num=self.num
        if interval is None:
            interval=self.interval
        for i in xrange(num):
            try:
                level.pattern[offset+i*interval].append(self.specs)
            except KeyError:
                level.pattern[offset+i*interval]=[self.specs]

#----------------------------------------------------------------------FUNCTIONS

def load_image(name, color_key=IMG_COLORKEY_DEF, scaling=IMG_SCALE_DEF):
    pathname=os.path.join(IMG_DIR,name+IMG_EXT)
    try:
        image=pygame.image.load(pathname)
    except pygame.error, msg:
        #print 'Error loading image %s' % name
        raise SystemExit, msg
    image=image.convert_alpha()
    if scaling!=1:
        image=scale(image, (int(image.get_size()[0]*scaling),
                            int(image.get_size()[1]*scaling)))
    #attempt to convert per-pixel to colorkey transparency for speed
    #w,h=image.get_size()
    #for x in xrange(w):
    #    for y in xrange(h):
    #        if image.get_at((x,y))[3]<ALPHA_THRESHOLD:
    #            image.set_at((x,y), color_key)
    #image=image.convert()
    #image.set_colorkey(color_key, RLEACCEL)
    return image

def load_all_images():
    for i in IMG_NAMES:
        images[i]=load_image(i)

def gcd(a, b):
    while b>0:
        a,b=b,a%b
    return a

def lcm(a, b):
    return a*b/gcd(a,b)
