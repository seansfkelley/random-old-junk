from aux import *
from game_obj import *
from math import sin, radians, log

#-------------------------------------------------------------movement functions
#parametric, t is the number of frames the unit has been alive
SF_DEF=         lambda t: Vector(0, -t*SHOT_SPD_Y_DEF)
SF_FAST=        lambda t: Vector(0, -t*SHOT_SPD_Y_DEF)
SF_LEFT=        lambda t: Vector(-24, -t*SHOT_SPD_Y_DEF)
SF_RIGHT=       lambda t: Vector(24, -t*SHOT_SPD_Y_DEF)
SF_ANGLE_LEFT=  lambda t: Vector(-6*t, -t*SHOT_SPD_Y_DEF)
SF_ANGLE_RIGHT= lambda t: Vector(6*t, -t*SHOT_SPD_Y_DEF)
SF_LEFT_SIN=    lambda t: Vector(32*sin(radians(24*t)), -t*SHOT_SPD_Y_DEF)
SF_RIGHT_SIN=   lambda t: Vector(-32*sin(radians(24*t)), -t*SHOT_SPD_Y_DEF)

EF_ASLT_LEFT=   lambda t: Vector(t, YRES+VERT_BUFFER-200-((t-30)/2)**2)
EF_ASLT_RIGHT=  lambda t: Vector(-6*log(t, 2), 35*log(t**3, 2))
EF_DEF=         lambda t: Vector(0, t*MOVE_SPEED_VERT/2)

#----------------------------------------------------------------firing patterns
#trailing , for 1-tuple
PTRN_DEF=   (0,{SHOT_INT_DEF: ((DMG_DEF, SHOT_NAME_DEF, SF_DEF),)}) 
PTRN_LASER= (0,{2:            ((DMG_DEF, SHOT_NAME_DEF, SF_FAST),),
                12:           ((DMG_DEF, SHOT_NAME_DEF, SF_LEFT),
                               (DMG_DEF, SHOT_NAME_DEF, SF_RIGHT))})
PTRN_TRI=   (0,{SHOT_INT_DEF: ((DMG_DEF, SHOT_NAME_DEF, SF_DEF),
                               (DMG_DEF, SHOT_NAME_DEF, SF_ANGLE_LEFT),
                               (DMG_DEF, SHOT_NAME_DEF, SF_ANGLE_RIGHT))})
PTRN_WAVE=  (0,{SHOT_INT_DEF: ((DMG_DEF, SHOT_NAME_DEF, SF_LEFT_SIN),
                               (DMG_DEF, SHOT_NAME_DEF, SF_RIGHT_SIN))})

#------------------------------------------------------------------swarms/levels
LEVELS=[Level() for i in xrange(NUM_LEVELS)]

swarm_straight=SwarmGen(((100, -VERT_BUFFER),\
    2, 'enemy', EF_ASLT_LEFT, ENEMY_MAX_Y_DEF, (.25,.25), False), 4, 20)
swarm_straight.generate(LEVELS[0], 90)
swarm_straight=SwarmGen(((XRES-100, -VERT_BUFFER),\
    2, 'enemy', EF_ASLT_RIGHT, ENEMY_MAX_Y_DEF, (.25,.25), True), 4, 20)
swarm_straight.generate(LEVELS[0], 90)

for l in LEVELS:
    l.find_max()

#to do
#scrolling background
#enemy shoot+collision test
#upgrades/bombs
#scoring/multipliers?
#temp. invulnerability (flashing?)
#more precise collision detection (with multiple parts?)
