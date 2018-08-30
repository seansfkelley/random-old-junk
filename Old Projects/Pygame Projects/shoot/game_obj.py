from aux import *

class Player:
    def __init__(self, start_pos, controls, flip_display):
        self.ship=DummyShip(controls)
        self.score=0
        self.controls=controls
        self.start=start_pos
        self.lives=LifeCount(flip_display)
        self.respawn_time=0
    def die(self):
        self.ship.die()
        tmp=self.lives.dec()
        if tmp:
            self.respawn_time=RESPAWN_TIME
        return tmp
    def respawn(self, instant=False):
        #hacky, can this be made nicer?
        self.respawn_time-=1
        if self.respawn_time==0 or instant:
            from specs import PTRN_DEF
            self.ship=Ship(self, self.start, self.controls, PTRN_DEF)
            if instant:
                self.respawn_time=0
    def reset(self):
        self.lives.reset()

class LifeCount:
    def __init__(self, flip):
        self.lives=0
        self.imgs=[]
        self.img_name='life'
        if flip:
            self.flip=-1
        else:
            self.flip=1
    def dec(self):
        self.lives-=1
        self.imgs[-1].kill()
        del self.imgs[-1]
        return self.lives>0
    def is_dead(self):
        return self.lives==0
    def reset(self):
        self.lives=NUM_LIVES
        spr=pygame.sprite.Sprite()
        spr.image=images[self.img_name]
        spr.rect=spr.image.get_rect()
        pos=Vector(LIFE_IMG_OFFSET[0]+spr.rect.w/2,\
                   LIFE_IMG_OFFSET[1]+spr.rect.h/2)
        if self.flip==-1:
            pos.x=XRES-pos.x
        spr.rect.center=pos.to_tuple()
        delta_x=(spr.rect.w+LIFE_SPACING)*self.flip
        self.imgs=[spr]
        life_group.add(spr)
        for i in xrange(NUM_LIVES-1):
            pos.x+=delta_x
            spr=pygame.sprite.Sprite()
            spr.image=images[self.img_name]
            spr.rect=spr.image.get_rect()
            spr.rect.center=pos.to_tuple()
            self.imgs.append(spr)
            life_group.add(spr)

class Ship(pygame.sprite.Sprite):
    def __init__(self, owner, pos, controls, wep_pattern):
        pygame.sprite.Sprite.__init__(self)
        self.owner=owner
        self.image=images['ship']
        self.rect=self.image.get_rect()
        self.rect.center=tuple(pos)
        self.vert=self.horiz=0
        self.firing=False
        self.interval=0
        self.weapon=Weapon(self, wep_pattern)
        
        self.UP,self.DOWN,self.LEFT,self.RIGHT,self.SHOOT=controls
        keysdown=pygame.key.get_pressed()
        for k in controls:
            if keysdown[k]:
                self.keydown(k)
        
        ship_group.add(self)
    def keydown(self, key):
        if key==self.UP:
            self.vert-=1
        elif key==self.DOWN:
            self.vert+=1
        elif key==self.LEFT:
            self.horiz-=1
        elif key==self.RIGHT:
            self.horiz+=1
        elif key==self.SHOOT:
            self.weapon.on()
        else:
            return False
        return True
    def keyup(self, key):
        if key==self.UP:
            self.vert+=1
        elif key==self.DOWN:
            self.vert-=1
        elif key==self.LEFT:
            self.horiz+=1
        elif key==self.RIGHT:
            self.horiz-=1
        elif key==self.SHOOT:
            self.weapon.off()
        else:
            return False
        return True
    def update(self):
        x,y=self.rect.center
        self.rect.center=(x+self.horiz*MOVE_SPEED_HORIZ,y+self.vert*MOVE_SPEED_VERT)
        self.rect.clamp_ip(VISIBLE_AREA)
        self.weapon.update()
    def die(self):
        self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, specs):
        pygame.sprite.Sprite.__init__(self)
        self.origin,self.life,img_name,self.movement,self.max_y,vary,collidable=specs
        self.image=images[img_name]
        self.rect=self.image.get_rect()
        self.rect.center=self.origin
        self.origin=Vector(self.origin)
        self.frames=0
        if self.max_y<=0:
            self.max_y=YRES+self.rect.h+1
        self.x_mod,self.y_mod=1-vary[0]*(random()*2-1),1-vary[1]*random()
        if collidable:
            enemy_group_collidable.add(self)
        enemy_group_all.add(self)
    def update(self):
        self.frames+=1
        temp=self.movement(self.frames)
        temp.x*=self.x_mod
        temp.y*=self.y_mod
        self.rect.center=(self.origin+temp).to_tuple()
        if self.rect.bottom>self.max_y:
            self.rect.bottom=self.max_y
        if not PLAY_AREA.colliderect(self.rect):
            self.kill()
    def damage(self, dmg):
        self.life-=dmg
        if self.life<=0:
            self.kill()

class Shot(pygame.sprite.Sprite):
    def __init__(self, pos, dmg, img_name, mov_func):
        pygame.sprite.Sprite.__init__(self)
        self.image=images[img_name]
        self.rect=self.image.get_rect()
        self.rect.center=tuple(pos)
        self.origin=Vector(pos)
        self.movement=mov_func
        self.frames=0
        self.damage=dmg
    def update(self):
        self.frames+=1
        self.rect.center=(self.origin+self.movement(self.frames)).to_tuple()
        if not PLAY_AREA.collidepoint(self.rect.midbottom):
            self.kill()
    def hurt(self, enemy):
        if self.alive():
            enemy.damage(self.damage)
            self.kill()

class Weapon:
    def __init__(self, ship, type):
        self.ship=ship
        self.firing=False
        self.frames=0
        self.start_value,self.shots=type
        self.intervals=self.shots.keys()
    def update(self):
        if self.firing:
            for i in self.intervals:
                if not self.frames%i:
                    self.fire(i)
            self.frames+=1
    def on(self):
        self.firing=True
        self.frames=self.start_value
    def off(self):
        self.firing=False
    def fire(self, which):
        for (dmg,img,func) in self.shots[which]:
            shot_group.add(Shot(self.ship.rect.midtop, dmg, img, func))

class Level:
    def __init__(self, pattern=None, max_frame=None):
        if pattern is None:
            pattern={}
        self.pattern=pattern
        if max_frame is None:
            max_frame=0
        self.max=max_frame
        self.frames=-1
    def update(self):
        self.frames+=1
        try:
            for specs in self.pattern[self.frames]:
                Enemy(specs)
        except KeyError:
            pass
        if self.max==self.frames:
            return False
        return True
    def find_max(self):
        self.max=max(self.pattern.keys())
