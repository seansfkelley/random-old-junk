from const import *
from aux import *

class Structure(pygame.sprite.Sprite):
    def __init__(self, key):
        pygame.sprite.Sprite.__init__(self)
        self.image=images[key]
        self.rect=self.image.get_rect()
        self.width=STR_WIDTHS[key]
        self.height=STR_HEIGHTS[key]
        self.cost=STR_COSTS[key]

class Floor(Structure):
    def __init__(self):
        Structure.__init__(self, 'floor')

class Buyable(Structure):
    def __init__(self, kind):
        Structure.__init__(self, kind)

class Office(Buyable):
    def __init__(self):
        Buyable.__init__(self, 'office')
