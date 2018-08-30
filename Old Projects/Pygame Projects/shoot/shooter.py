#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

from aux import *
from game_obj import *
from specs import *

def handle_input(events, p1, p2):
    for e in events:
        if e.type==KEYDOWN and not p1.ship.keydown(e.key) and not p2.ship.keydown(e.key):
            if e.key==P1_START_BUTTON and p1.lives.is_dead():
                p1.reset()
                p1.respawn(True)
            elif e.key==P2_START_BUTTON and p2.lives.is_dead():
                p2.reset()
                p2.respawn(True)
        elif e.type==KEYUP and not p1.ship.keyup(e.key) and not p2.ship.keyup(e.key):
            pass
        elif e.type==QUIT:
            sys.exit(0)

def handle_input_gameover(events):
    for e in events:
        if e.type==KEYDOWN and not p1.keydown(e.key) and not p2.keydown(e.key):
            pass
        elif e.type==KEYUP and not p1.keyup(e.key) and not p2.keyup(e.key):
            pass
        elif e.type==QUIT:
            sys.exit(0)

pygame.init()

window=pygame.display.set_mode((XRES,YRES), DIS_FLAGS)
pygame.display.set_caption(NAME)
screen=pygame.display.get_surface()

background=pygame.Surface(screen.get_size()).convert()
background.fill((0,0,0))

load_all_images()
p1=Player(P1_START_POS, P1_CONTROLS, False)
p2=Player(P2_START_POS, P2_CONTROLS, True)

clock=pygame.time.Clock()

level_count=0

while True:
    clock.tick(FRAMERATE)
    
    handle_input(pygame.event.get(), p1, p2)
    
    if level_count<NUM_LEVELS:
        if not LEVELS[level_count].update():
            print 'level %d finished' % (level_count+1)
            level_count+=1
        
    shot_group.update()
    enemy_shot_group.update()
    enemy_group_all.update()
    ship_group.update()
    
    collisions=pygame.sprite.groupcollide(enemy_group_all, shot_group, False, False)
    for enemy in collisions:
        for s in collisions[enemy]:
            s.hurt(enemy)
            
    collisions=pygame.sprite.groupcollide(ship_group, enemy_group_collidable, False, False)
    for ship in collisions:
        if collisions[ship]:
            collisions[ship][0].damage(DMG_COLLIDE)
            if ship.owner.die():
                ship.owner.respawn()
            else:
                print 'you are out of lives'
                
    if p1.respawn_time:
        p1.respawn()
    if p2.respawn_time:
        p2.respawn()
    
    screen.blit(background, (0,0))
    
    #these 4 lines dictate which things appear on top of which
    enemy_shot_group.draw(screen)
    shot_group.draw(screen)
    enemy_group_all.draw(screen)
    ship_group.draw(screen)
    life_group.draw(screen)
    
    pygame.display.flip()
