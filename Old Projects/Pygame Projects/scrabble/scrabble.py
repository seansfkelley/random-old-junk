#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

from aux import *
from game_obj import *

def handle_input(events):
    for e in events:
        if e.type==QUIT:
            sys.exit(0)
        if e.type==MOUSEBUTTONDOWN:
            screen.blit(letter_imgs[LETTERS.keys()[randint(0, 26)]], e.pos)

pygame.init()

window=pygame.display.set_mode((XRES,YRES), DIS_FLAGS)
pygame.display.set_caption(NAME)
screen=pygame.display.get_surface()

clock=pygame.time.Clock()

tile_bkrd=load_image(BKRD_NAME)
font=pygame.font.Font(FONTNAME, LETTER_SIZE)

for l in LETTERS:
    letter_imgs[l]=tile_bkrd.copy()
    tmp=font.render(l, True, LETTER_COLOR)
    letter_imgs[l].blit(tmp, LETTER_OFFSET)
    all_letters+=[l]*LETTERS[l][0]

while True:
    clock.tick(FRAMERATE)
    handle_input(pygame.event.get())
    pygame.display.flip()
