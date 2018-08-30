#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

#to do
    #actual menu, variable options
    #other modes - times, etc
    #repeated (grid?) background
    #how to fade end of game text?
    #high score - display, input, output
    #enforce minimum size?
    #make sure header and other images are too too large

#py2applet --resources=images,OratorStd.otf --iconfile=icon.icns --make-setup Chain\ Shot\!.py

from aux import *
from game_obj import *
from pygame import font

elapsed_time=0
current_fade=0
current_text_fade=0
current_diff=MIN_DIFFICULTY
current_size=GRID_SIZE_DEF

num_dict={K_0:0,
          K_1:1,
          K_2:2,
          K_3:3,
          K_4:4,
          K_5:5,
          K_6:6,
          K_7:7,
          K_8:8,
          K_9:9}

def handle_input(events, play_zone):
    global elapsed_time, current_fade, current_text_fade, current_diff
    for e in events:
        if e.type==QUIT:
            sys.exit(0)
        elif e.type==MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]: #0 is left (button 0)
            if play_zone.game_over:
                play_zone.reset(current_diff)
                screen.blit(play_zone.screen, (0,0))
                pygame.display.flip()
                elapsed_time=0
                current_fade=0
                current_text_fade=0
            else:
                play_zone.process_click(pygame.mouse.get_pos())
        elif e.type==KEYDOWN:
            if num_dict.get(e.key, 0)>=MIN_DIFFICULTY:
                current_diff=num_dict[e.key]
                play_zone.reset(current_diff)
                screen.blit(play_zone.screen, (0,0))
                pygame.display.flip()
                elapsed_time=0
                current_fade=0
                current_text_fade=0

if BLOCK_SIZE>BLOCK_IMAGE_SIZE:
    print "Block size too large, limiting to %d." % BLOCK_IMAGE_SIZE
    BLOCK_SIZE=BLOCK_IMAGE_SIZE

pygame.init()

window=pygame.display.set_mode((XRES,YRES), DIS_FLAGS)
pygame.display.set_caption(NAME)
screen=pygame.display.get_surface()

load_all_images()

if BLOCK_SIZE!=BLOCK_IMAGE_SIZE:
    scale_factor=float(BLOCK_SIZE)/BLOCK_IMAGE_SIZE
    new_size=(scale_factor*images[COLORS[0]].get_width(), scale_factor*images[COLORS[0]].get_height())
    for c in COLORS:
        images[c]=scale(images[c], new_size)

background=background.convert(background)
overlay=overlay.convert_alpha(overlay)
fade_overlay=fade_overlay.convert_alpha(fade_overlay)

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

#load high scores
try:
    high_scores=pickle.load(open('highscores.dat'))
except IOError:
    pass

play_grid=PlayGrid(current_diff)
screen.blit(play_grid.screen, (0,0))
pygame.display.flip()

clock=pygame.time.Clock()

header_font=font.Font(HEADER_FONT_NAME, HEADER_FONT_SIZE)
time_offset=(XRES/2+TEXT_CENTER_OFFSET, TEXT_TOP_OFFSET)
score_x_offset=XRES/2.0-TEXT_CENTER_OFFSET

message_font=font.Font(MESSAGE_FONT_NAME, MESSAGE_FONT_SIZE)

while True:
    clock.tick(FRAMERATE)
    
    handle_input(pygame.event.get(), play_grid)
    
    play_grid.update()
    screen.blit(play_grid.screen, (0,0))
        
    screen.blit(overlay, (0, 0))
    time_disp=header_font.render('%02d:%02d' % (elapsed_time/60000, elapsed_time/1000%60), True, FONT_COLOR)
    screen.blit(time_disp, time_offset)
    score_disp=header_font.render('%d' % play_grid.score, True, FONT_COLOR)
    screen.blit(score_disp, (score_x_offset-score_disp.get_width(), TEXT_TOP_OFFSET))
    
    if play_grid.game_over:
        if not play_grid.win:
            fade_overlay.fill(FADE_COLOR+[current_fade])
            screen.blit(fade_overlay, (0,0))
            if current_fade<FADE_MAX:
                current_fade+=FADE_SPEED
                message_disp=pygame.Surface((0,0))
            else:
                if current_text_fade<255:
                    current_text_fade+=GO_TEXT_FADE_SPEED
                message_disp=message_font.render('You lose.', True, FONT_COLOR)
        else:
            if current_text_fade<255:
                current_text_fade+=GO_TEXT_FADE_SPEED
            message_disp=message_font.render('You win!', True, FONT_COLOR)
        screen.blit(message_disp, (XRES/2-message_disp.get_width()/2,
                                   YRES/2-message_disp.get_height()/2))
    else:
        elapsed_time+=clock.get_time()
    
    pygame.display.flip()
