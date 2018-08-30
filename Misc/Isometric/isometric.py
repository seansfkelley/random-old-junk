# Terms used in this program:
# cartesian coordinates: regular x/y coordinates. Not every cartesian x/y corresponds to a valid isometric grid space.
# isometric coordinates: currently ill-defined.

import pygame
import random
import heapq

NAME = 'Isometric'
 
LEFT_BUTTON, RIGHT_BUTTON = 1, 3

pygame.init()

SCREEN_SIZE = (1024, 768)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

CLOCK = pygame.time.Clock()

FRAMERATE = 30

g_game_running = True
g_start_click = None
g_current_path = None
 
pygame.display.set_caption(NAME)

GRID_SIZE = (16 + 1, 48 + 1)

# Need one extra space to account for offset of isometric display by a half tile in each direction.

TILE = pygame.image.load(open('/Users/sk/Documents/Programming/Isometric/tile.png'))
TILE_PATH = TILE_HIGHLIGHT = pygame.image.load(open('/Users/sk/Documents/Programming/Isometric/tile-highlight.png'))

TILE_X, TILE_Y = 64, 32
TILE_X_HALF, TILE_Y_HALF = TILE_X / 2, TILE_Y / 2

class PathFinder:
    def __init__(self, start, end):
        self._path = g_grid.find_path(start, end)
        for coords in self._path:
            g_grid[coords] = TILE_PATH
    
    def clear_path(self):
        for coords in self._path:
            g_grid[coords] = TILE

# Represents an isometric grid internally in a way that is easy to manipulate but requires mapping of
# coordinates and uses extra space. The grid should never be accessed directly.
class IsometricGrid:
    # Internal organization for a 3 by 4 (x by y) grid:
    # 3a  3b  3c
    #   2a  2b  2c 
    # 1a  1b  1c 
    #   0a  0b  0c
    # We produce the corresponding list:
    # [[0a, 1a, 2a, 3a], [0b, 1b, 2b, 3b], [0c, 1c, 2c, 3c]]
    # So that spaces may be indexed by [x][y].
    # Tiles will be drawn back-to-front, but the bottom left corner is still considered the origin.
    # Neighbors for x, y (with even y, clockwise, from top left) are computed via (x, y + 1), (x + 1, y + 1), (x + 1, y - 1), (x, y - 1)
    # for odd y, neighbors are (x - 1, y + 1), (x, y + 1), (x, y - 1), (x - 1, y - 1)
    
    # A globally-accessible tile offset. Change this to change what part of the grid is visible, as per the description
    # on draw(). Negatives are allowed.
    offset = [0, 0]
    
    # x_size = # of columns, y_size = # rows, fill_func is a function that takes two cartesian coordinates and returns
    # terrain (most usually an anonymous function tied to a particular loaded map data file).
    def __init__(self, x_size, y_size, fill_func):
        self._x, self._y = x_size, y_size
        
        self._grid = [[fill_func(x, y) for y in xrange(y_size)] for x in xrange(x_size)]
    
    # Returns the coordinates of the NW, NE, SE, SW neighbors of the given coordinate pair, in tile coordinates.
    # Guaranteed to return in that order. Coordinates are NOT guaranteed to be in the valid playable range.
    def neighbors(self, (x, y)):
        if y % 2:
            return (x, y + 1), (x + 1, y + 1), (x + 1, y - 1), (x, y - 1)
        return (x - 1, y + 1), (x, y + 1), (x, y - 1), (x - 1, y - 1)
    
    # Returns if the tile coordinates x, y are in the valid playable range.
    def in_bounds(self, (x, y)):
        return 0 <= x < self._x and 0 <= y < self._y
    
    def absolute_to_isometric(self, (Px, Py)):
        # Scale the points so we're working with a equilateral isometric grid. Equivalently, produce coordinates in
        # a new grid space in which each space is composed of exactly two adjacent isometric diamond quadrants.
        x, y = Px / TILE_X_HALF, Py / TILE_Y_HALF
        
        if x % 2 == y % 2:
            # In the case that they're both even or odd, the dividing line between the two quadrants goes top left -> 
            # bottom right. This can be seen if the pattern is drawn out. Ay represents the y-coordinate of the left
            # point of the dividing diagonal in absolute coordinates.
            # Additionally, in the later formula the term (By - Ay) is calculated, where By is the y-coordinate of the
            # right point of the dividing diagonal. This can be simplified to (+/-) TILE_Y_HALF, since we know the
            # dividing diagonal occupies exactly one grid box. By_Ay represents this value. (The sign changing depending
            # on which of the two grid box types we are in right now).
            Ay = (y + 1) * TILE_Y_HALF
            By_Ay = -TILE_Y_HALF
        else:
            # Conversely, these grid boxes have the dividing lines go bottom left -> top right.
            Ay = y * TILE_Y_HALF
            By_Ay = TILE_Y_HALF
        
        # Check which side of the line the point falls on (i.e. which of the two quadrants it's in).
        # (Bx - Ax) * (Py - Ay) - (By - Ay) * (Px - Ax)
        # Where the line is (left-to-right) A-to-B and the point is P.
        if TILE_X_HALF * (Py - Ay) - By_Ay * (Px - (x * TILE_X_HALF)) < 0:
            # Depending on which type of grid box we are looking at, we need to use the which-side-of-the-line
            # calculation in a different way. I do not have a satisfactory mathematical explanation for these operations,
            # but they were derived by examining a drawn-out diagram of each of the four possible combinations.
            if x % 2 == y % 2:
                return x / 2, y
            else:
                return (x + 1) / 2, y
        else:
            if x % 2 == y % 2:
                return (x + 1) / 2, y + 1
            else:   
                return x / 2, y + 1
    
    # Compute the pixel coordinates in absolute space of the given screen-space coordinates. Includes origin
    # conversion and offsetting for the currently visible grid area.
    def screen_to_absolute(self, (x, y)):
        y = SCREEN_SIZE[1] - y
        return x + self.offset[0] * TILE_X, y + self.offset[1] * TILE_Y_HALF
    
    # 
    def find_path(self, start, end):
        def h((x0, y0), (x1, y1)):
            return abs(x0 - x1) + abs(y0 - y1)
        
        def reconstruct():
            path = [end]
            while path[-1] is not start:
                path.append(predecessors[path[-1]])
            path.reverse()
            return path
        
        closed_set = set()
        open_set = set((start,))
        closest_tiles = [(h(start, end), start)]
        predecessors = {}
        
        known_costs = {start : 0}
        
        while open_set:
            score, coords = heapq.heappop(closest_tiles)
            print coords, end
            if coords == end:
                return reconstruct()
            
            open_set.remove(coords)
            closed_set.add(coords)
            
            new_cost = known_costs[coords] + 1
            for n in filter(self.in_bounds, self.neighbors(coords)):
                print 'checking', n
                if n in closed_set:
                    print 'closed set'
                    continue
                if self[n] is not TILE:
                    print 'not tile'
                    continue
                if n not in open_set:
                    open_set.add(n)
                    heapq.heappush(closest_tiles, (new_cost + h(n, end), n))
                    predecessors[n] = coords
                    known_costs[n] = new_cost
                elif new_cost < known_costs[n]:
                    # Should-be-lgn decrease_key turns out to be linear! Why isn't this part of the heapq library?
                    for i in xrange(len(closest_tiles)):
                        if closest_tiles[i][1] == n:
                            closest_tiles[i] = (new_cost, n)
                            break
                    heapq.heapify(closest_tiles)
                    predecessors[n] = coords
                    known_costs[n] = new_cost
        
        return []
    
    # Retrieve the element at the given tile coordinates. Assumed to be a valid coordinate pair.
    def __getitem__(self, (x, y)):
        return self._grid[x][y]
    
    # Set the element at the given tile coordinates. Assumed to be a valid coordinate pair and value.
    def __setitem__(self, (x, y), v):
        self._grid[x][y] = v
    
    # Draw enough tiles to fill the screen. Draw the portion of the grid visible when the current grid offset holds
    # the coordinate of the tile to be visible in the bottom-left corner of the drawn screen. Drawn back-to-front. 
    # The offset's y is rounded down to the nearest even value before drawing. Tiles that don't exist (i.e. the 
    # offset causes coordinates to be checked that are not valid) will be ignored.
    def draw(self):
        mouse = self.absolute_to_isometric(self.screen_to_absolute(pygame.mouse.get_pos()))
        
        x_origin, y_origin = self.offset
        if y_origin % 2: y_origin -= 1
        cur_rect = pygame.Rect(-TILE_X / 2, -TILE_Y / 2, TILE_X, TILE_Y)
        for y in xrange(y_origin + SCREEN_SIZE[1] / TILE_Y_HALF, y_origin - 1, -1):
            for x in xrange(x_origin, x_origin + SCREEN_SIZE[0] / TILE_X + 1):
                if self.in_bounds((x, y)):
                    if (x, y) == mouse:
                        SCREEN.blit(TILE_HIGHLIGHT, cur_rect)
                    elif self._grid[x][y]:
                        SCREEN.blit(self._grid[x][y], cur_rect)
                cur_rect.left += TILE_X
            
            cur_rect.left = -TILE_X / 2 if y % 2 else 0
            cur_rect.top += TILE_Y / 2
    


g_change_tile_to = None

def handle_events():
    global g_game_running, g_start_click, g_current_path
    g_click_pos = None
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            g_game_running = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            coords = g_grid.absolute_to_isometric(g_grid.screen_to_absolute(e.pos))
            if e.button == LEFT_BUTTON and g_grid[coords] is TILE:
                if g_start_click is not None:
                    g_grid[g_start_click] = TILE
                g_start_click = coords
            elif e.button == RIGHT_BUTTON and g_grid[coords] is TILE and g_start_click is not None:
                if g_current_path is not None:
                    g_current_path.clear_path()
                g_current_path = PathFinder(g_start_click, coords)
                g_start_click = None
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                g_grid.offset[0] -= 1
            elif e.key == pygame.K_RIGHT:
                g_grid.offset[0] += 1
            elif e.key == pygame.K_DOWN:
                g_grid.offset[1] -= 2
            elif e.key == pygame.K_UP:
                g_grid.offset[1] += 2

def update_state():
    pass

def draw_screen():
    SCREEN.fill((255, 255, 255))
    g_grid.draw()


g_grid = IsometricGrid(GRID_SIZE[0], GRID_SIZE[1], lambda x, y: TILE if random.randint(0, 1) else None)

while g_game_running:
    handle_events()
    update_state()
    draw_screen()
 
    CLOCK.tick(FRAMERATE)
    pygame.display.flip()

pygame.quit()