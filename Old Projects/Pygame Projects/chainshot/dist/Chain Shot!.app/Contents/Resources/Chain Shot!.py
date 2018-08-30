#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

#to do
    #actual menu, variable options
    #other modes - times, etc
    #repeated (grid?) background

#py2applet --resources=images,OratorStd.otf --iconfile=icon.icns --make-setup Chain\ Shot\!.py

from aux import *
from game_obj import *
from pygame import font

elapsed_time=0

def handle_input(events, play_zone):
    for e in events:
        if e.type==QUIT:
            sys.exit(0)
        elif e.type==MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]: #0 is left (button 0)
            if play_zone.game_over:
                play_zone.reset(DIFFICULTY_DEF)
                screen.blit(play_zone.screen, (0,0))
                pygame.display.flip()
                global elapsed_time
                elapsed_time=0
            else:
                play_zone.process_click(pygame.mouse.get_pos())

pygame.init()

window=pygame.display.set_mode((XRES,YRES), DIS_FLAGS)
pygame.display.set_caption(NAME)
screen=pygame.display.get_surface()

load_all_images()

background=background.convert(background)
overlay=overlay.convert_alpha(overlay)

#create overlay
overlay.fill((0,0,0,0)) #fill with transparent

temp_surface=scale(images['bot_corner'], (HOR_OVR_BORDER, BOT_OVR_BORDER))
overlay.blit(temp_surface, (0, overlay.get_height()-BOT_OVR_BORDER))
temp_surface=pygame.transform.flip(temp_surface, True, False)
overlay.blit(temp_surface, (XRES-HOR_OVR_BORDER, YRES-BOT_OVR_BORDER))

temp_surface=scale(images['bottom'], (XRES-2*HOR_OVR_BORDER, BOT_OVR_BORDER))
overlay.blit(temp_surface, (HOR_OVR_BORDER, YRES-BOT_OVR_BORDER))

temp_surface=scale(images['side'], (HOR_OVR_BORDER, YRES-BOT_OVR_BORDER-TOP_OVR_BORDER_TOTAL))
overlay.blit(temp_surface, (0, TOP_OVR_BORDER_TOTAL))
temp_surface=pygame.transform.flip(temp_surface, True, False)
overlay.blit(temp_surface, (XRES-HOR_OVR_BORDER, TOP_OVR_BORDER_TOTAL))

temp_surface=scale(images['top_corner'], (HOR_OVR_BORDER, TOP_OVR_BORDER_BUFFER))
overlay.blit(temp_surface, (0, TOP_OVR_BORDER_MAIN))
temp_surface=pygame.transform.flip(temp_surface, True, False)
overlay.blit(temp_surface, (XRES-HOR_OVR_BORDER, TOP_OVR_BORDER_MAIN))

temp_surface=scale(images['top'], (XRES-2*HOR_OVR_BORDER, TOP_OVR_BORDER_BUFFER))
overlay.blit(temp_surface, (HOR_OVR_BORDER, TOP_OVR_BORDER_MAIN))

temp_surface=pygame.Surface((XRES, TOP_OVR_BORDER_MAIN))
temp_surface.fill(HEADER_FILL)
if SCALE_HEADER:
    temp_surface.blit(scale(images['header'], (XRES, TOP_OVR_BORDER_MAIN)), (0,0))
else:
    temp_surface.blit(images['header'], ((XRES-images['header'].get_width())/2.0,
                                         (TOP_OVR_BORDER_MAIN-images['header'].get_height())/2.0))

overlay.blit(temp_surface, (0, 0))

play_grid=PlayGrid(DIFFICULTY_DEF)
screen.blit(play_grid.screen, (0,0))
pygame.display.flip()

clock=pygame.time.Clock()

font_display=font.Font(FONT_NAME, FONT_SIZE)
time_offset=(XRES/2+TEXT_CENTER_OFFSET, TEXT_TOP_OFFSET)
score_x_offset=XRES/2.0-TEXT_CENTER_OFFSET

elapsed_time=0

while True:
    clock.tick(FRAMERATE)
    elapsed_time+=clock.get_time()
    
    handle_input(pygame.event.get(), play_grid)
    
    play_grid.update()
    screen.blit(play_grid.screen, (0,0))
        
    screen.blit(overlay, (0, 0))
    time_disp=font_display.render('%02d:%02d' % (elapsed_time/60000, elapsed_time/1000%60), True, FONT_COLOR)
    screen.blit(time_disp, time_offset)
    score_disp=font_display.render('%d' % play_grid.score, True, FONT_COLOR)
    screen.blit(score_disp, (score_x_offset-score_disp.get_width(), TEXT_TOP_OFFSET))
    pygame.display.flip()
