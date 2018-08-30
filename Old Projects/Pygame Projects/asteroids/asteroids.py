#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

import pygame, sys, os, math
from pygame.locals import *
from random import randint

XRES,YRES=800,800
FRAMERATE=30

SAFE_RADIUS=200
NUM_LIVES=3
DELAY=60 #frames
INVULN=90
BLINK_FREQ=6
ACCEL=.4 #pixels/frame^2
DECEL=.1
BRAKE=.6
ROTATION=5 #degress/frame
TOP_SPEED=12 #in pixels/frame

SHOT_SPEED=16
SHOT_LIFE=40
MAX_SHOTS=6

ROID_DELAY=30 #frames
ROID_INIT=3 #initial amounts
ROID_PER_LEVEL=2 #additional per level
ROID_SPLIT=2 #asteroid babies :O
ROID_LOW_SPEED=2
ROID_HIGH_SPEED=6
ROID_SCORES=(100,40,10)

SHIP_SCALE=.33
SHOT_SCALE=.25
ROID_SCALE=(1.25, .75, .33)
TITLE_SIZE=72
SCORE_SIZE=20

sprites=pygame.sprite.Group()
shots=pygame.sprite.Group()
asteroids=pygame.sprite.Group()

playing=False
level=-1
lives=NUM_LIVES
title_font=score_font=None
ship=None
blank=None
moves=None
asteroid_images=[]
life_indicators=[]
ship_image=None
shot_image=None
shot_rect=None
num_shots=0
roid_delaying=0
delaying=0
score=0

pygame.init()

if not pygame.font.get_init():
    raise SystemExit

window=pygame.display.set_mode((XRES,YRES))
pygame.display.set_caption('Asteroids')
screen=pygame.display.get_surface()

scale=pygame.transform.smoothscale
rotate=pygame.transform.rotate

def load_image(name, color_key=None, scaling=1):
    pathname=os.path.join('data',name)
    try:
        image=pygame.image.load(open(pathname))
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
    return (image, image.get_rect())

def handle_input(eventlist):
    global delaying, playing
    for event in eventlist:
        if event.type==QUIT:
            sys.exit(0)
        if not playing:
            if event.type==MOUSEBUTTONDOWN and event.button==1:
                playing=True
                ship=Ship()
        else:
            if event.type==KEYDOWN and not delaying:
                try:
                    moves[event.key](1)
                except KeyError:
                    pass
            if event.type==KEYUP and not delaying:
                try:
                    moves[event.key](0)
                except KeyError:
                    pass

def make_asteroids():
    global level
    level+=1
    for i in xrange(ROID_INIT+level*ROID_PER_LEVEL):
        a=Asteroid(0)
        if ship:
            while math.sqrt((a.rect.center[0]-ship.rect.center[0])**2+
                            (a.rect.center[1]-ship.rect.center[1])**2)<SAFE_RADIUS:
                a.rect.center=(randint(0,XRES),randint(0,YRES))

def bound_movement(pos):
    return ((pos[0]+XRES)%XRES, (pos[1]+YRES)%YRES)

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=ship_image
        self.rect=self.image.get_rect()
        self.original=self.image.copy()
        self.rect.center=(XRES/2, YRES/2)
        self.invuln=INVULN
        self.before_blink=None
        self.blank=False
        self.blink=0
        self.speed=0
        self.facing=90
        self.up=self.down=self.left=self.right=0
        
        global moves
        moves={ord('w'):self.toggle_up,
               ord('a'):self.toggle_left,
               ord('s'):self.toggle_down,
               ord('d'):self.toggle_right,
               ord(' '):self.shoot}
        sprites.add(self)
        
    def update(self):
        "moves the ship on-screen according to several factors"
        if self.invuln>0:
            self.invuln-=1
            self.blink=(self.blink+1)%BLINK_FREQ
            if self.blink==0:
                if self.blank:
                    self.image=self.before_blink
                else:
                    self.before_blink=self.image
                    self.image=blank
                self.blank=not self.blank
            if self.invuln==0:
                self.image=self.before_blink
                self.blank=False
                
        
        pos=self.rect.center
        
        self.facing=(self.facing+(self.right+self.left)*ROTATION+360)%360
        rad=math.radians(self.facing)
        
        if not self.blank:
            self.image=rotate(self.original, self.facing)
        
        self.rect=self.image.get_rect()
        self.rect.center=pos
        
        if self.down:
            self.speed-=BRAKE
            if self.speed<0:
                self.speed=0
        elif self.up:
            self.speed+=ACCEL
            if self.speed>TOP_SPEED:
                self.speed=TOP_SPEED
        else:
            self.speed-=DECEL
            if self.speed<0:
                self.speed=0
        
        self.rect.move_ip(math.cos(rad)*self.speed, -math.sin(rad)*self.speed)
        self.rect.center=bound_movement(self.rect.center)
        
        if self.invuln==0:     
            collisions=pygame.sprite.spritecollide(self, asteroids, False)
            if collisions:
                for a in collisions:
                    a.explode()
                self.explode()
    
    def toggle_up(self, toggle):
        self.up=toggle
    
    def toggle_down(self, toggle):
        self.down=toggle
            
    def toggle_right(self, toggle):
        self.right=-toggle

    def toggle_left(self, toggle):
        self.left=toggle
    
    def shoot(self, toggle):
        global num_shots
        if toggle==1 and num_shots<MAX_SHOTS:
            Shot(self.rect.center, math.radians(self.facing))
            num_shots+=1
    
    def explode(self):
        global lives, delaying, ship
        self.kill()
        ship=None
        lives-=1
        life_indicators[lives].kill()
        if lives!=0:
            delaying=DELAY

class Shot(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image=shot_image.copy()
        self.rect=pygame.Rect(shot_rect)
        self.rect.center=tuple(position)
        self.dir=direction
        self.life=SHOT_LIFE
        
        sprites.add(self)
        shots.add(self)
        
    def update(self):
        global num_shots
        self.rect.move_ip(math.cos(self.dir)*SHOT_SPEED,
                          -math.sin(self.dir)*SHOT_SPEED)
        self.rect.center=bound_movement(self.rect.center)
        self.life-=1
        if self.life==0:
            num_shots-=1
            self.kill()
            
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)
        index=randint(0, len(asteroid_images)-1)
        self.image=asteroid_images[index].copy()
        self.image=scale(self.image, (int(self.image.get_size()[0]*ROID_SCALE[level]),
                                      int(self.image.get_size()[1]*ROID_SCALE[level])))
        self.image=rotate(self.image, randint(0,359))
        self.rect=self.image.get_rect()
        self.rect.center=(randint(0,XRES),randint(0,YRES))
        self.speed=randint(ROID_LOW_SPEED, ROID_HIGH_SPEED)
        self.dir=math.radians(randint(0,359))
        self.level=level
        
        asteroids.add(self)
        sprites.add(self)
    
    def update(self):
        self.rect.move_ip(math.cos(self.dir)*self.speed,
                          -math.sin(self.dir)*self.speed)
        self.rect.center=bound_movement(self.rect.center)
        l=pygame.sprite.spritecollide(self, shots, True)
        if l:
            global num_shots
            num_shots-=len(l)
            self.explode()
        
    def explode(self):
        global score
        if self.level<len(ROID_SCALE)-1:
            for i in xrange(ROID_SPLIT):
                a=Asteroid(self.level+1)
                a.rect.center=tuple(self.rect.center)
        self.kill()
        score+=ROID_SCORES[self.level]
        if not asteroids:
            global roid_delaying
            roid_delaying=ROID_DELAY
        
def main():
    global blank, ship_image, shot_image, shot_rect,\
           sprites, ship, lives, delaying, roid_delaying,\
           title_font, score_font, playing

    background=pygame.Surface(screen.get_size())
    background=background.convert()
    background.fill((0,0,0))
    
    pathname=os.path.join('data','Vectorb.ttf')
    title_font=pygame.font.Font(open(pathname), TITLE_SIZE)
    score_font=pygame.font.Font(open(pathname), SCORE_SIZE)
    
    ship_image,rect=load_image('ship.png', -1, SHIP_SCALE)
    blank=pygame.Surface((1,1))
    blank=blank.convert()
    blank.fill((0,0,0))
    ship_image=rotate(ship_image, -90)
    
    shot_image, shot_rect=load_image('shot.png', -1, SHOT_SCALE)
    
    try:
        i=0
        while True:
            image,rect=load_image('asteroid%d.png' % i, -1, ROID_SCALE[0])
            asteroid_images.append(image)
            i+=1
    except IOError:
        if i!=0:
            pass
        else:
            raise SystemExit

    make_asteroids()
    clock=pygame.time.Clock()
    
    for i in xrange(NUM_LIVES):
        l=pygame.sprite.Sprite()
        l.image=rotate(ship_image, 90)
        l.rect=l.image.get_rect()
        l.rect.center=(l.rect.width*(i+2), 2*l.rect.height)
        sprites.add(l)
        life_indicators.append(l)
        
    score_pos=(2*l.rect.width-9, l.rect.height)
        
    title=title_font.render('ASTEROIDS', False, (255,255,255))
    w,h=title_font.size('ASTEROIDS')
    title_pos=((XRES-w)/2,(YRES-h)/2)
   
    while True:
        clock.tick(FRAMERATE)
        handle_input(pygame.event.get())
        screen.blit(background, (0,0))
        if not playing:
            asteroids.update()
            asteroids.draw(screen)
            screen.blit(title, title_pos)
        else:
            sprites.update()
            sprites.draw(screen)
            score_display=score_font.render('%.6d' % score, False, (255,255,255))
            screen.blit(score_display, score_pos)
        pygame.display.flip()
        if roid_delaying:
            roid_delaying-=1
            if roid_delaying==0:
                make_asteroids()
        if delaying:
            delaying-=1
            if delaying==0:
                ship=Ship()
        if lives==0:
            print 'game over placeholder'
            lives=-1


if __name__=='__main__':
    main()
