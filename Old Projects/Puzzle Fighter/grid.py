from constants import *

import pygame

class KeySet:
    def __init__(self):
        self.left = self.right = self.drop = self.cw = self.ccw = None
    


class Grid(pygame.sprite.AbstractGroup):
    def __init__(self, real_offset, key_set, blockqueue):
        pygame.sprite.AbstractGroup.__init__(self)
        
        self.offset_x, self.offset_y = real_offset
        self.key_set = key_set
        self.blockqueue = blockqueue
        
        self.queue_index = 0
        self.blockpair = None
        self.grid = [[None] * ROWS for i in xrange(COLS)]
    
    def add(self, block):
        self.grid[block.grid_x][block.grid_y] = block
        pygame.sprite.AbstractGroup.add(self, block)
    
    def remove(self, block):
        self.grid[block.grid_x][block.grid_y] = None
        pygame.sprite.AbstractGroup.remove(self, block)
    
    def draw(self, screen):
        for s in self.sprites():
            s.draw(screen)
    
    # Have a timer so that the blockpair has to be stationary for a few frames before it settles permanently.
    
    def update(self):
        if self.blockpair == None:
            # Explosions!
            self.next_pair()
        else:
            self.blockpair.fall()
        
        pygame.sprite.AbstractGroup.update(self)
    
    def free_space(self, x, y):
        return x > -1 and x < COLS and y > -1 and y < ROWS and self.grid[x][y] == None
    
    def clear_block(self, x, y):
        self.grid[x][y] = None
    
    def set_block(self, block, x, y):
        self.grid[x][y] = block
    
    def grid_to_real(self, grid_coords):
        return (grid_coords[0] * BLOCK_SIZE + self.offset_x, grid_coords[1] * BLOCK_SIZE + self.offset_y)
    
    def real_to_grid(self, real_coords):
        return ((real_coords[0] - self.offset_x) / BLOCK_SIZE, (real_coords[1] - self.offset_y) / BLOCK_SIZE)
    
    def key_down(self, key):
        if self.blockpair == None:
            return
        if key == self.key_set.left:
            self.blockpair.left()
        elif key == self.key_set.right:
            self.blockpair.right()
        elif key == self.key_set.cw:
            self.blockpair.rotate_cw()
        elif key == self.key_set.ccw:
            self.blockpair.rotate_ccw()
    
    def key_up(self, key):
        pass
    
    def next_pair(self):
        self.blockpair = self.blockqueue.next(self)
    
