#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

from const import *
from interface import *

pygame.init()

window=pygame.display.set_mode((XRES,YRES), DIS_FLAGS)
pygame.display.set_caption('SimTower')
screen=pygame.display.get_surface()

load_all_images()
calc_borders()

clock=pygame.time.Clock()

tower=Tower((XRES,YRES))

while True:
    clock.tick(FRAMERATE)
    if handle_input(pygame.event.get(), tower):
        screen=pygame.display.set_mode(tower.bkrd.get_size(), DIS_FLAGS)
    screen.blit(tower.bkrd, (0,0))
    tower.update()
    tower.draw(screen)
    pygame.display.flip()
