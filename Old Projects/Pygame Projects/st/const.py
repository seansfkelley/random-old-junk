import pygame, sys, os
from pygame.locals import *
from random import randint

#gameplay
STR_NAMES=['floor','lobby','office','condo']
STR_K=    [K_f,    K_l,    K_o,     K_c]
STR_W=    [1,      4,      6,       12]
STR_H=    [1,      1,      1,       1]
STR_C=    [500,    250,    20000,   150000]

STR_KEYS=dict(zip(STR_K, STR_NAMES))
STR_WIDTHS=dict(zip(STR_NAMES, STR_W))
STR_HEIGHTS=dict(zip(STR_NAMES, STR_H))
STR_COSTS=dict(zip(STR_NAMES, STR_C))

#visuals
XRES,YRES=800,600
WIDTH,HEIGHT=8,32
DIS_FLAGS=RESIZABLE
BORDER_COLOR=(200,200,255)
BORDER_WIDTH=1
BORDERS={}

#internal/functional
FRAMERATE=30
IMG_EXT='.png'
IMG_DIR='images'

#aliases
scale=pygame.transform.smoothscale

#globals
images={}
