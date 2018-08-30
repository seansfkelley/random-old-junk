from aux import *
import random

#origin is topleft (for grid too)

class Block(pygame.sprite.Sprite):
    def __init__(self, color=None, position=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.color=color
        self.pos=position
        self.x_offset=0
        self.y_offset=0
        self.image=images[color]
        self.rect=self.image.get_rect()
        self.rect.bottomleft=pos_to_coords(position)
        
    def __str__(self):
        return 'Block (%s) @ (%d, %d)/(%d, %d)' % (self.color, self.pos[0], self.pos[1], self.rect.left, self.rect.bottom)

class PlayGrid:
    def __init__(self, difficulty):
        self.score=0
        self.moving=[]
        self.num_to_remove=0
        self.destroyed=False
        self.game_over=False
        self.win=False
        self.screen=pygame.Surface((XRES,YRES)).convert()
        self.draw_list=[]
        self.grid=[]
        for x in xrange(GRID_SIZE_DEF[0]):
            temp=[]
            for y in xrange(GRID_SIZE_DEF[1]):
                temp.append(Block(COLORS[random.randint(1, difficulty)-1], (x, y)))
                temp[-1].y_offset=x*INTRO_SPACING+(GRID_SIZE_DEF[1]-y-1)*GRID_SIZE_DEF[0]*INTRO_SPACING+INTRO_CONST_HEIGHT
                temp[-1].rect.bottom-=temp[-1].y_offset
                self.moving.append(temp[-1])
            self.grid.append(list(temp))
            temp.reverse()
            self.draw_list+=temp
        
        self.draw()
    
    def reset(self, difficulty):
        self.__init__(difficulty)
    
    def calc_game_over(self):
        self.game_over=True
        for x in xrange(len(self.grid)):
            for y in xrange(len(self.grid[0])):
                if self.valid(x, y) and len(self.neighbors(x, y, [], self.grid[x][y].color))>1:
                    self.game_over=False
                    break
    
    def valid(self, x, y):
        return 0<=x<=len(self.grid)-1 and 0<=y<=len(self.grid[0])-1 and self.grid[x][y]!=None
            
    def process_click(self, coords):
        if self.moving:
            return
        x,y=coords_to_pos(coords)
        if self.valid(x, y):
            n=self.neighbors(x, y, [], self.grid[x][y].color)
            if len(n)>1: #includes original block
                self.destroy(n)
        
    def neighbors(self, x, y, ns, c):
        if self.valid(x, y) and self.grid[x][y].color==c and self.grid[x][y] not in ns:
            ns.append(self.grid[x][y])
            self.neighbors(x-1, y, ns, c)
            self.neighbors(x+1, y, ns, c)
            self.neighbors(x, y-1, ns, c)
            self.neighbors(x, y+1, ns, c)
        return ns
        
    def destroy(self, neighbors):
        self.score+=(len(neighbors)-1)**2
        for n in neighbors:
            x,y=coords_to_pos(n.rect.center)
            
            #calculate falling blocks
            for i in xrange(y):
                if self.valid(x, i):
                    self.grid[x][i].y_offset+=BLOCK_SIZE
                    if self.grid[x][i] not in neighbors and self.grid[x][i] not in self.moving:
                        self.moving.append(self.grid[x][i])
                        
            self.grid[x][y]=None
            self.draw_list.remove(n)
        
        #calculate sliding blocks
        for x in xrange(len(self.grid)):
            empty=True
            for y in xrange(len(self.grid[0])):
                if self.grid[x][y]!=None:
                    empty=False
                    break
            if empty:
                self.num_to_remove+=1
                for slide_x in xrange(x+1, len(self.grid)):
                    for slide_y in xrange(0, len(self.grid[0])):
                        if self.valid(slide_x, slide_y):
                            self.grid[slide_x][slide_y].x_offset+=BLOCK_SIZE
                            if self.grid[slide_x][slide_y] not in neighbors and self.grid[slide_x][slide_y] not in self.moving:
                                self.moving.append(self.grid[slide_x][slide_y])
        
        for b in self.moving:
            self.grid[b.pos[0]][b.pos[1]]=None
        
        self.destroyed=True
        
    def update(self):
        refresh=self.moving or self.destroyed
        if self.moving:
            to_remove=[]
            for b in self.moving:
                if b.x_offset==0 and b.y_offset==0:
                    to_remove.append(b)
                    b.pos=coords_to_pos(b.rect.center)
                    self.grid[b.pos[0]][b.pos[1]]=b
                else:
                    if b.x_offset!=0:
                        b.x_offset-=SLIDE_SPEED
                        if b.x_offset<0:
                            b.rect.left-=(SLIDE_SPEED+b.x_offset)
                            b.x_offset=0
                        else:
                            b.rect.left-=SLIDE_SPEED
                    if b.y_offset!=0:
                        b.y_offset-=FALL_SPEED
                        if b.y_offset<0:
                            b.rect.bottom+=(FALL_SPEED+b.y_offset)
                            b.y_offset=0
                        else:
                            b.rect.bottom+=FALL_SPEED
            for b in to_remove:
                self.moving.remove(b)
        elif self.destroyed:
            if self.num_to_remove>0:
                for i in xrange(self.num_to_remove):
                    self.grid.pop()
                self.num_to_remove=0
            self.calc_game_over()
            if self.game_over:
                if len(self.draw_list)==0:
                    self.score=int(self.score*WIN_BONUS)
                    self.win=True
                else:
                    self.win=False
            self.destroyed=False
        if refresh:
            self.draw()
        
    def draw(self):
        self.screen.blit(background, (0,0))
        for b in self.draw_list:
            self.screen.blit(b.image, b.rect)
