import pygame, sys, os, pickle
from pygame.locals import *

#----------------------------------------------------------------------CONSTANTS

#------------------------------------------------------------------------visuals
DIS_FLAGS=0
COLORS=['red','blue','yellow','green','orange','purple','black','teal','pink']
OVERLAYS=['top','bottom','side','top_corner','bot_corner','header']

HEADER_FONT_NAME='./OratorStd.otf'
HEADER_FONT_SIZE=36
MESSAGE_FONT_NAME='./OratorStd.otf'
MESSAGE_FONT_SIZE=48
FONT_COLOR=(255,255,255)

BLOCK_IMAGE_SIZE=64 #do NOT change this unless the block images change

BLOCK_SIZE=64
BKRD_DEFAULT=(127,127,127)

#-----------------------------------------------------------------------gameplay
MIN_DIFFICULTY=3
GRID_SIZE_DEF=(7,9)
WIN_BONUS=1.25

#--------------------------------------------------------------internal settings
HOR_WIN_BORDER=8
TOP_WIN_BORDER=116
BOT_WIN_BORDER=8

HOR_OVR_BORDER=16
TOP_OVR_BORDER_MAIN=100
TOP_OVR_BORDER_BUFFER=16
TOP_OVR_BORDER_TOTAL=TOP_OVR_BORDER_MAIN+TOP_OVR_BORDER_BUFFER
BOT_OVR_BORDER=16

HEADER_FILL=(0,0,0)
SCALE_HEADER=False

TEXT_CENTER_OFFSET=92
TEXT_TOP_OFFSET=56

FADE_COLOR=[0,0,0]
FADE_MAX=100
FADE_SPEED=3

GO_TEXT_FADE_SPEED=5

PLAY_X,PLAY_Y=BLOCK_SIZE*GRID_SIZE_DEF[0], BLOCK_SIZE*GRID_SIZE_DEF[1]
XRES,YRES=PLAY_X+2*HOR_WIN_BORDER, PLAY_Y+TOP_WIN_BORDER+BOT_WIN_BORDER
FALL_SPEED=32 #px/frame
SLIDE_SPEED=16
INTRO_SPACING=16
INTRO_CONST_HEIGHT=64

FRAMERATE=30
IMG_EXT='.png'
IMG_DIR='images'

#---------------------------------------------------------------------------misc
NAME='Chain Shot!'

#------------------------------------------------------------------------aliases
scale=pygame.transform.smoothscale
rotate=pygame.transform.rotate

#------------------------------------------------------------------------globals
images={}
high_scores={}
background=pygame.Surface((XRES, YRES))
background.fill(BKRD_DEFAULT)
overlay=pygame.Surface((XRES, YRES))
fade_overlay=pygame.Surface((XRES, YRES))

#----------------------------------------------------------------------FUNCTIONS

def load_image(name):
    pathname=os.path.join(IMG_DIR,name+IMG_EXT)
    try:
        image=pygame.image.load(pathname)
    except pygame.error, msg:
        #print 'Error loading image %s' % name
        raise SystemExit, msg
    image=image.convert_alpha()
    return image

def load_all_images():
    for i in COLORS+OVERLAYS:
        images[i]=load_image(i)

def pos_to_coords(x, y=None):
    if y==None:
        x,y=x #to allow tuples
    return (x*BLOCK_SIZE+HOR_WIN_BORDER, (y+1)*BLOCK_SIZE+TOP_WIN_BORDER)

def coords_to_pos(x, y=None):
    if y==None:
        x,y=x
    return (int((x-HOR_WIN_BORDER)/BLOCK_SIZE), int((y-TOP_WIN_BORDER)/BLOCK_SIZE))
