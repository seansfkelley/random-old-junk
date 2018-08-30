from constants import *
from pygame.locals import *
from globals import *

import os
import pygame
import sys

def load_image(name):
    pathname = os.path.join(IMG_DIR, name + IMG_EXT)
    try:
        image = pygame.image.load(open(pathname))
    except pygame.error, msg:
        raise SystemExit, msg
    image = image.convert_alpha()
    return image


def load_all_images():
    for i in COLORS:
        g_all_images[PREFIX_SMALL + i] = load_image(PREFIX_SMALL + i)
        g_all_images[PREFIX_CRASH + i] = load_image(PREFIX_CRASH + i)


def handle_input():
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit(0)
        elif e.type == KEYDOWN:
            g_grid_player_1.key_down(e.key)
            g_grid_player_2.key_down(e.key)
        elif e.type == KEYUP:
            g_grid_player_1.key_up(e.key)
            g_grid_player_2.key_up(e.key)

