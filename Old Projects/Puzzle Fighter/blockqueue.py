from constants import *
from random import randint
from blockpair import BlockPair

class BlockQueue:
    def __init__(self):
        self.class_queue = []
        self.color_queue = []
    
    def next(self, grid):
        if grid.queue_index >= len(self.class_queue):
            self.extend()
        pivot = self.class_queue[grid.queue_index](self.color_queue[grid.queue_index], grid, (3, 1))
        orbit = self.class_queue[grid.queue_index + 1](self.color_queue[grid.queue_index + 1], grid, (3, 0))
        grid.queue_index += 2
        grid.add(pivot)
        grid.add(orbit)
        return BlockPair(pivot, orbit)
    
    def extend(self):
        from gems import Gem, CrashGem
        
        for i in xrange(10):
            self.class_queue.append(Gem)
            self.color_queue.append(COLORS[randint(0, len(COLORS) - 1)])
    
