from globals import *
from constants import *
from gems import *
from auxiliary import load_all_images, handle_input

import pygame

pygame.init()

window = pygame.display.set_mode((XRES, YRES), DIS_FLAGS)
pygame.display.set_caption(NAME)
screen = pygame.display.get_surface()

load_all_images()

while True:
    g_game_clock.tick(FRAMERATE)
    
    handle_input()
    
    g_grid_player_1.update()
    g_grid_player_2.update()
    
    screen.fill((0, 0, 0))
    
    g_grid_player_1.draw(screen)
    g_grid_player_2.draw(screen)
    
    pygame.display.flip()