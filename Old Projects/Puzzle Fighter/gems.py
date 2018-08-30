from constants import *
from animatedsprite import AnimatedSprite
from globals import g_all_images

import pygame

class Block(AnimatedSprite):
    def __init__(self, grid, grid_position = (0, 0)):
        AnimatedSprite.__init__(self)
        
        self.grid = grid
        self.grid_x, self.grid_y = grid_position
        self.rect.topleft = self.grid.grid_to_real(grid_position)
    
    def can_move_grid(self, dx, dy):
        return self.grid.free_space(self.grid_x + dx, self.grid_y + dy)
    
    def move_sprite(self, dx, dy):
        self.rect.left += dx
        self.rect.top += dy
    
    def move_grid(self, dx, dy):
        self.grid.clear_block(self.grid_x, self.grid_y)
        self.grid_x += dx
        self.grid_y += dy
        self.grid.set_block(self, self.grid_x, self.grid_y)
        self.move_sprite(dx * BLOCK_SIZE, dy * BLOCK_SIZE)
    
    def set_sprite(self, x, y):
        self.rect.left = x
        self.rect.top = y
    
    def set_grid(self, x, y):
        self.grid.clear_block(self.grid_x, self.grid_y)
        self.x = x
        self.y = y
        self.grid.set_block(self, self.grid_x, self.grid_y)
    
    def __str__(self):
        return "%s (%d, %d)" % (self.__class__.__name__, self.grid_x, self.grid_y)


class Gem(Block):
    def __init__(self, color, grid, grid_position = (0, 0)):
        Block.__init__(self, grid, grid_position)
        
        self.exploding = False
        self.color = PREFIX_SMALL + color
        self.change_image(g_all_images[self.color], 1, 1)
    
    def explode(self):
        self.exploding = True
        
        for n in self.grid.neighbors(self.grid_position):
            if not n.exploding:
                n.explode()
    


class CrashGem(Gem):
    def __init__(self, color, grid, grid_position = (0, 0)):
        Gem.__init__(self, color, grid, grid_position)
        
        self.color = PREFIX_CRASH + color
        self.change_image(g_all_images[self.color], CRASH_FRAMES, CRASH_FPS)
    
