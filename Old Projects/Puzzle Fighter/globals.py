from constants import *
from pygame.locals import *

import pygame
import grid
import blockqueue

g_all_images = {}
g_game_clock = pygame.time.Clock()

g_controls_player_1 = grid.KeySet()
g_controls_player_1.left = K_a
g_controls_player_1.right = K_d
g_controls_player_1.drop = K_s
g_controls_player_1.cw = K_e
g_controls_player_1.ccw = K_q

g_controls_player_2 = grid.KeySet()
g_controls_player_2.left = K_l
g_controls_player_2.right = K_QUOTE
g_controls_player_2.drop = K_SEMICOLON
g_controls_player_2.cw = K_LEFTBRACKET
g_controls_player_2.ccw = K_o

g_block_queue = blockqueue.BlockQueue()

g_grid_player_1 = grid.Grid((BORDER_LEFT, BORDER_TOP), g_controls_player_1, g_block_queue)
g_grid_player_2 = grid.Grid((BORDER_LEFT + COLS * BLOCK_SIZE + MIDDLE_SPACING, BORDER_TOP), g_controls_player_2, g_block_queue)