import pygame, sys, os
from pygame.locals import *
from random import randint

def load_image(name, color_key=None, scaling=1):
    pathname=os.path.join(IMG_DIR,name+IMG_EXT)
    try:
        image=pygame.image.load(pathname)
    except pygame.error, msg:
        #print 'Error loading image %s' % name
        raise SystemExit, msg
    image=image.convert()
    if color_key:
        if color_key==-1:
            color_key=image.get_at((0,0))
        image.set_colorkey(color_key, RLEACCEL)
    if scaling!=1:
        image=scale(image, (int(image.get_size()[0]*scaling),
                            int(image.get_size()[1]*scaling)))
    return image

XRES,YRES=600,600
DIS_FLAGS=0
NAME='Scrabble'
FRAMERATE=30
BKRD_NAME='tile_background'
IMG_DIR='images'
IMG_EXT='.png'
FONTNAME='LucidaGrande.dfont'
LETTER_OFFSET=7,1
LETTER_SIZE=24
LETTER_COLOR=(0,0,0)
NUM_LETTERS=7

#letter:(amount,points)

LETTERS={'A':(9,1),
         'B':(2,3),
         'C':(2,3),
         'D':(4,2),
         'E':(12,1),
         'F':(2,4),
         'G':(3,2),
         'H':(2,4),
         'I':(9,1),
         'J':(1,8),
         'K':(1,5),
         'L':(4,1),
         'M':(2,3),
         'N':(6,1),
         'O':(8,1),
         'P':(2,3),
         'Q':(1,10),
         'R':(6,1),
         'S':(4,1),
         'T':(6,1),
         'U':(4,1),
         'V':(2,4),
         'W':(2,4),
         'X':(1,8),
         'Y':(2,4),
         'Z':(1,10),
         ' ':(2,0)}
      
letter_imgs={}
all_letters=[]
