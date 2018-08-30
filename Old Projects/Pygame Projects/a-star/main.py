import math
import pygame
import sys
import quadtree
import astar
import pickle # pickle is awesome.

from pygame.locals import *
from astar_constants import *

#display/interactivity constants
RESOLUTION = 512

CLICK_PATHING={
	K_4: PATH_WALKABLE,
	K_5: PATH_SWIMMABLE,
	K_6: PATH_FLYABLE
}

CLICK_UNIT=K_u
CLICK_ADJACENT=K_a

KEY_PAUSE=K_p
KEY_SAVE=K_s
KEY_OPEN=K_o
KEY_QUIT=K_q
KEY_CLOSE=K_w

GRID_COLOR=(0,0,0)
UNIT_COLOR=(127,127,127)
SOLUTION_COLOR=(200,200,200)
SELECTION_COLOR=(0,127,0)
VOID_COLOR=(127,127,127)

USE_GRID=False

UNIT_SIZE=16
UNIT_SPEED=3

#setup display variables
pygame.init()

g_screen=pygame.display.set_mode((RESOLUTION, RESOLUTION))
g_background=pygame.Surface((RESOLUTION, RESOLUTION))
g_clock=pygame.time.Clock()

# g_arrows={}

#setup background and other images
g_solution_marker=pygame.Surface((UNIT_SIZE, UNIT_SIZE), SRCALPHA)
g_solution_marker.fill((0,0,0,0))
pygame.draw.circle(g_solution_marker, SOLUTION_COLOR, (UNIT_SIZE/2, UNIT_SIZE/2), UNIT_SIZE/8)
g_solution_marker=g_solution_marker.convert_alpha()

g_unit_marker=pygame.Surface((UNIT_SIZE, UNIT_SIZE), SRCALPHA)
g_unit_marker.fill((0,0,0,0))
pygame.draw.circle(g_unit_marker, UNIT_COLOR, (UNIT_SIZE/2, UNIT_SIZE/2), UNIT_SIZE/4)
g_unit_marker=g_unit_marker.convert_alpha()

g_selection_circle=pygame.Surface((UNIT_SIZE, UNIT_SIZE), SRCALPHA)
g_selection_circle.fill((0,0,0,0))
pygame.draw.circle(g_selection_circle, SELECTION_COLOR, (UNIT_SIZE/2, UNIT_SIZE/2), UNIT_SIZE/4+2)
pygame.draw.circle(g_selection_circle, (0,0,0,0), (UNIT_SIZE/2, UNIT_SIZE/2), UNIT_SIZE/4)
g_selection_circle=g_selection_circle.convert_alpha()

# temp=pygame.Surface((7,8), SRCALPHA)
# temp.fill((0,0,0,0))
# for (start, end) in (((2,7),(2,1)), ((3,7),(3,0)), ((4,7),(4,1)), ((0,3),(6,3)), ((1,2),(5,2))):
# 	pygame.draw.line(temp, UNIT_COLOR, start, end)
# 
# g_arrows['up']=temp.convert_alpha()
# g_arrows['left']=pygame.transform.rotate(temp, 90).convert_alpha()
# g_arrows['down']=pygame.transform.rotate(temp, 180).convert_alpha()
# g_arrows['right']=pygame.transform.rotate(temp, 270).convert_alpha()

#interactivity variables
g_click_type=None
g_adding_obstacles=True
g_unit_selected=None
g_units=pygame.sprite.Group()
g_moving=False

g_integer=0

g_node_images={}

def gen_node_image_from(node):
	if node.botleft:
		gen_node_image_from(node.botleft)
		gen_node_image_from(node.botright)
		gen_node_image_from(node.topleft)
		gen_node_image_from(node.topright)
	else:
		image=pygame.Surface((node.size, node.size), SRCALPHA)
		if node.pathing&PATH_VOID:
			image.fill(VOID_COLOR)
		else:
			color=[0,255,0]
			if node.pathing&PATH_WALKABLE:
				color[0]=255
			if node.pathing&PATH_SWIMMABLE:
				color[1]=0
			if node.pathing&PATH_FLYABLE:
				color[2]=255
		image.fill(color)
		pygame.draw.lines(image, GRID_COLOR, True, ((0,0), (node.size-1, 0), (node.size-1, node.size-1), (0, node.size-1)))
		g_node_images[node]=image.convert_alpha()

def generate_quad_background(node, surface=None):
	if surface==None:
		surface=pygame.Surface((node.size, node.size), SRCALPHA)
	if node.botleft:
		generate_quad_background(node.botleft, surface)
		generate_quad_background(node.botright, surface)
		generate_quad_background(node.topleft, surface)
		generate_quad_background(node.topright, surface)
	else:
		surface.blit(g_node_images[node], (node.x, RESOLUTION-node.y-node.size))
	return surface


def flip_screen_logical_coords(coords):
	return (coords[0], RESOLUTION-coords[1])


def line_of_sight(grid, src, dst):
	global g_integer
	
	g_integer=0
	m=slope(src, dst)
	
	x_increase, y_increase = dst[0]>src[0], dst[1]>src[1]
	
	# intersections with horizontal gridlines
	if m!=0:
		if math.isnan(m):
			dx=0
		else:
			dx=1/m
		if y_increase:
			# dx = dx # y = src[1]+1; (y-src[1])/m
			x = src[0] + .5 + dx/2 # .5 to begin from center of grid space, dx/2 to find first collision
			for y in xrange(src[1]+1, dst[1]+1):
				g_integer+=1
				grid_x_pos=int(x) # floor the int, because grid spaces are located by their bottom left integers
				# print 'checking y=%d and %d, x=%d' % (y, y-1, grid_x_pos)
				if grid[grid_x_pos, y].pathing==PATH_OBSTACLE or grid[grid_x_pos, y-1].pathing==PATH_OBSTACLE:
					return False # print 'fail at x = %f' % x
				x+=dx
		else:
			dx = -dx # y = src[1]-1; (y-src[1])/m
			x = dst[0] + .5 - dx/2 # .5 to begin from center of grid space, dx/2 to find first collision
			for y in xrange(dst[1]+1, src[1]+1):
				g_integer+=1
				grid_x_pos=int(x) # floor the int, because grid spaces are located by their bottom left integers
				# print 'checking y=%d and %d, x=%d' % (y, y-1, grid_x_pos)
				if grid[grid_x_pos, y].pathing==PATH_OBSTACLE or grid[grid_x_pos, y-1].pathing==PATH_OBSTACLE:
					return False # print 'fail at x = %f' % x
				x-=dx
	
	# intersections with vertical gridlines
	if not math.isnan(m):
		if x_increase:
			dy = m # by definition - for x = 1, mx = m, thus dy = m
			y = src[1] + .5 + dy/2
			for x in xrange(src[0]+1, dst[0]+1):
				g_integer+=1
				grid_y_pos=int(y)
				# print 'checking x=%d and %d, y=%d' % (x, x-1, grid_y_pos)
				if grid[x, grid_y_pos].pathing==PATH_OBSTACLE or grid[x-1, grid_y_pos].pathing==PATH_OBSTACLE:
					return False # print 'fail at y = %f' % y
				y+=dy
		else:
			dy = -m # same, but in opposite direction
			y = dst[1] + .5 - dy/2
			for x in xrange(dst[0]+1, src[0]+1):
				g_integer+=1
				grid_y_pos=int(y)
				# print 'checking x=%d and %d, y=%d' % (x, x-1, grid_y_pos)
				if grid[x, grid_y_pos].pathing==PATH_OBSTACLE or grid[x-1, grid_y_pos].pathing==PATH_OBSTACLE:
					return False # print 'fail at y = %f' % y
				y-=dy
	
	return True


#A* variables
g_quad=quadtree.QuadNode((0,0), RESOLUTION)
#quadtree.randomize(g_quad)
gen_node_image_from(g_quad)
g_background=generate_quad_background(g_quad).convert_alpha()
g_search=astar.AStarSearch(g_quad)

#interactivity structures
class Unit(pygame.sprite.Sprite):
	def __init__(self, coords):
		pygame.sprite.Sprite.__init__(self)
		self.image=g_unit_marker.convert_alpha()
		self.rect=self.image.get_rect()
		self.rect.center=coords
		self.goal=(0,0)
		self.nodes=[]
		self.path=[]
		self.index=1
		self.current_node=self.goal
		self.target_coords=None
		self.movement_type=PATH_WALKABLE
	
	def __str__(self):
		return 'Unit: (%d, %d)->(%d, %d)=%d' %\
		(self.current_node.x, self.current_node.y, self.goal.x, self.goal.y, len(self.path))
	
	def reset_for_search(self):
		self.start=flip_screen_logical_coords(self.rect.center)
		self.current_node=g_quad.locate(flip_screen_logical_coords(self.rect.center))
	
	def create_path(self):
		if not self.nodes:
			print 'No path found.'
			return
		self.index=1
		self.direction=1
		self.path=[]
		self.path.append(flip_screen_logical_coords(self.start))
		for i in xrange(len(self.nodes)-1):
			self.path.append(flip_screen_logical_coords(quadtree.contact_center(self.nodes[i], self.nodes[i+1])))
		self.path.append(flip_screen_logical_coords(self.goal))
		self.target_coords=self.path[1]
	
	def update(self):
		if g_moving and self.path:
			x_dist=float(self.target_coords[0]-self.rect.center[0])
			y_dist=float(self.target_coords[1]-self.rect.center[1])
			real_dist=math.sqrt(x_dist**2 + y_dist**2)
			if real_dist<UNIT_SPEED:
				if 0<self.index<len(self.path)-1:
					self.index+=self.direction
				else:
					self.direction=-self.direction
					self.index+=self.direction
				self.target_coords=self.path[self.index]
				return
			x_move=int((x_dist/real_dist)*UNIT_SPEED) # basically, cos*speed
			y_move=int((y_dist/real_dist)*UNIT_SPEED) # sin*speed
			self.rect.bottomleft = self.rect.left+x_move, self.rect.bottom+y_move


def minimize_quad_at(quadnode, xy):
	try:
		while True:
			quadnode.split()
			quadnode=quadnode.locate(xy)
	except ValueError:
		pass
	return quadnode


def process_events():
	global g_click_type, g_search, g_adding_obstacles, g_unit_selected, g_moving, g_quad, g_background
	for e in pygame.event.get():
		if e.type==QUIT:
			sys.exit(0)
			
		# possible to use event.get_mods or similar instead of global pygame.get_mods?
		elif e.type==KEYDOWN and pygame.key.get_mods()&KMOD_META:
			if e.key==KEY_PAUSE:
				g_moving=not g_moving
			elif e.key==KEY_SAVE:
				f=open('map', 'wb')
				p=pickle.Pickler(f, 2)
				p.dump(g_quad)
				f.close()
			elif e.key==KEY_OPEN:
				up=pickle.Unpickler(open('map', 'rb'))
				g_quad=up.load()
				gen_node_image_from(g_quad)
				g_background=generate_quad_background(g_quad).convert_alpha()
				g_search.map=g_quad
			elif e.key==KEY_QUIT or e.key==KEY_CLOSE:
				sys.exit(0)
			else:
				g_click_type=e.key
			
		elif e.type==MOUSEBUTTONDOWN:
			if e.button==1: #left
				g_unit_selected=None
				for u in g_units.sprites():
					if u.rect.collidepoint(e.pos):
						g_unit_selected=u
						break
						
				if not g_unit_selected:
					click_loc=flip_screen_logical_coords(e.pos)
					quad_node=g_quad.locate(click_loc)
					if g_click_type==CLICK_ADJACENT:
						quadtree.find_adjacent(quad_node, g_quad)
						for a in quad_node.adjacent:
							print a
					
					elif g_click_type==CLICK_UNIT and quad_node.pathing&PATH_WALKABLE:
						u=Unit(e.pos)
						g_units.add(u)
						g_unit_selected=u
					
					elif g_click_type in CLICK_PATHING:
						qn=minimize_quad_at(quad_node, click_loc)
						g_adding_obstacles=not bool(qn.pathing&CLICK_PATHING[g_click_type])
						qn.pathing^=CLICK_PATHING[g_click_type]
						qn.simplify()
						gen_node_image_from(g_quad)
						g_background=generate_quad_background(g_quad).convert_alpha()
								
			elif e.button==3: #right
				if g_unit_selected:
					g_unit_selected.reset_for_search()
					g_unit_selected.goal=flip_screen_logical_coords(e.pos)
					g_unit_selected.nodes=g_search.search(g_unit_selected.start, g_unit_selected.goal, g_unit_selected.movement_type)
					g_unit_selected.create_path()
					
		elif e.type==MOUSEMOTION and pygame.mouse.get_pressed()[0]:
			move_loc=flip_screen_logical_coords(e.pos)
			if g_click_type in CLICK_PATHING:
				qn=minimize_quad_at(g_quad.locate(move_loc), move_loc)
				if g_adding_obstacles:
					qn.pathing|=CLICK_PATHING[g_click_type]
				else:
					qn.pathing&=invert_pathing(CLICK_PATHING[g_click_type])
				qn.simplify()
				gen_node_image_from(g_quad)
				g_background=generate_quad_background(g_quad).convert_alpha()


#begin main loop
while True:
    process_events()
    g_clock.tick(30)
    g_screen.blit(g_background, (0,0))
    g_units.update()
    g_units.draw(g_screen)
    for u in g_units:
    	if len(u.path)>1:
    		pygame.draw.lines(g_screen, GRID_COLOR, False, u.path)
    if g_unit_selected:
    	g_screen.blit(g_selection_circle, g_unit_selected.rect.topleft)
    pygame.display.flip()

### strange center-contact behavior, sometimes it hugs walls
### have separate pathing maps for each pathing type?
### implement brush size - 1 2 4 8 16...
### cross product from current best/current to goal? or from start to goal?
### unit collision size for quadtree
### pathfind using corners and edges as well as center coordinates?
### open set should use a heap
### save resolution and check when opening maps for compatibility

#to do:
#	path optimization - one spline for each quad node?
#	convert LoS simplification, or use new method?
#	break off simplification or tail-end pathfinding into separate thread?
#	penalize crossed paths in cost functions?
#	make units move all the way to the end -> len() condition in update() is not letting it complete
#	get as close as possible if end is occupied or path is totally blocked

#	get python-ogre working (xcode?)! and then incorporate this
#	rewrite in c++ for speed/learning python bindings?