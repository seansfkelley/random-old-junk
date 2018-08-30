from const import *
from structs import *

def handle_input(events, tower):
    resize=False
    for e in events:
        if e.type==QUIT:
            sys.exit(0)
        elif e.type==KEYDOWN:
            try:
                tower.set_type(STR_KEYS[e.key])
            except KeyError:
                if e.key==K_SPACE:
                    tower.unset_type()
        elif e.type==VIDEORESIZE:
            tower.bkrd=pygame.Surface(e.size).convert()
            tower.bkrd.fill((0,0,0))
            resize=True
    return resize

class Tower(pygame.sprite.Group):
    def __init__(self, size):
        pygame.sprite.Group.__init__(self)
        self.bkrd=pygame.Surface(size).convert()
        self.bkrd.fill((0,0,0))
        self.cursor=None
        self.current_type=None
    def update(self):
        if self.cursor:
            #snap building border to grid
            r=self.cursor.rect
            x, y=pygame.mouse.get_pos()
            x, y=x-r.w/2, y-r.h/2
            x_diff, y_diff=x%WIDTH, y%HEIGHT
            if x_diff>=WIDTH/2:
                r.left=x-x_diff+WIDTH
            else:
                r.left=x-x_diff
            if y_diff>=HEIGHT/2:
                r.top=y-y_diff+HEIGHT
            else:
                r.top=y-y_diff
    def set_type(self, which):
        if self.cursor:
            self.unset_type()
        self.current_type=which
        self.cursor=BORDERS[which]
        self.add(self.cursor)
    def unset_type(self):
        self.current_type=None
        self.cursor.kill()
