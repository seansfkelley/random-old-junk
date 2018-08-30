import grid

from constants import *
from random import randint

RANDOM_OBSTACLES=400
GROW_CHANCE=80

NORTH, EAST, WEST, SOUTH = 0, 1, 2, 3
OPPOSITE_DIR=lambda x: 3-x

class MeshNode:
	def __init__(self, x, y):
		self.indices=(x, y)
		self.adjacent=[None]*4
	



class MeshPolygon:
	def __init__(self):
		pass
	



class NavigationMesh:
	def __init__(self, grid):
		self.grid=grid
		self.calculate_mesh()
	
	def calculate_mesh(self):
		self.node_mesh=[[None]*(Y_LENGTH+1) for j in xrange(X_LENGTH+1)]
		
		# check corners
		if self.grid[0, 0].kind==KIND_NORMAL:
			self.node_mesh[0][0]=True # MeshNode()
		if self.grid[X_LENGTH-1, 0].kind==KIND_NORMAL:
			self.node_mesh[X_LENGTH][0]=True # MeshNode()
		if self.grid[X_LENGTH-1, Y_LENGTH-1].kind==KIND_NORMAL:
			self.node_mesh[X_LENGTH][Y_LENGTH]=True # MeshNode()
		if self.grid[0, Y_LENGTH-1].kind==KIND_NORMAL:
			self.node_mesh[0][Y_LENGTH]=True # MeshNode()
		
		# check edges
		for x in xrange(1, X_LENGTH):
			if self.grid[x-1,0].kind==KIND_NORMAL or self.grid[x,0].kind==KIND_NORMAL:
				self.node_mesh[x][0]=True # MeshNode()
			if self.grid[x-1,Y_LENGTH-1].kind==KIND_NORMAL or self.grid[x,Y_LENGTH-1].kind==KIND_NORMAL:
				self.node_mesh[x][Y_LENGTH]=True # MeshNode()
		for y in xrange(1, Y_LENGTH):
			if self.grid[0,y-1].kind==KIND_NORMAL or self.grid[0,y].kind==KIND_NORMAL:
				self.node_mesh[0][y]=True # MeshNode()
			if self.grid[X_LENGTH-1,y-1].kind==KIND_NORMAL or self.grid[X_LENGTH-1,y].kind==KIND_NORMAL:
				self.node_mesh[X_LENGTH][y]=True # MeshNode()
		
		# check middle
		for x in xrange(1, X_LENGTH):
			for y in xrange(1, Y_LENGTH):
				bordering_squares=(self.grid[x, y], self.grid[x-1, y], self.grid[x-1, y-1], self.grid[x, y-1])
				for i in xrange(1,4):
					if bordering_squares[i-1].kind!=bordering_squares[i].kind:
						self.node_mesh[x][y]=True # MeshNode()
		
		first=None
		for x in xrange(X_LENGTH+1):
			for y in xrange(Y_LENGTH+1):
				if self.node_mesh[x][y]:
					first=(x,y)
					break
			if first:
				break
		
		self.side_queue=[]
		# self.find_polygon(first)
	
	
	# roll these functions into a self-tracking MeshPolygon?
	def valid_moves(self, current, previous=None):
		pass
		# this function finds which of the 8 directions are valid and orders them according to preference
		#if previous:
			# try to continue along same path, how to know which side is valid and which isnt?
	
	def find_polyon(self, xy0, xy1=None):
		# basically, call valid_moves repeatedly and store each answer proressively to allow backtracking
		# xy0 ist he start point for a polygon, xy1 is the other point if this polygon is using an
		#  already-defined side from another polygon
		pass
	




def randomize(grid):
	x, y=randint(0,X_LENGTH-1), randint(0,Y_LENGTH-1)
	grid[x,y].kind=KIND_OBSTACLE
	num_obstacles=0
	
	while num_obstacles<RANDOM_OBSTACLES:
		if randint(0,99)<GROW_CHANCE:
			offset=((1,0), (-1,0), (0,1), (0,-1))[randint(0,3)]
			x, y=x+offset[0], y+offset[1]
			if x>=0 and y>=0 and x<X_LENGTH and y<Y_LENGTH and grid[x,y].kind!=KIND_OBSTACLE:
				grid[x,y].kind=KIND_OBSTACLE
				num_obstacles+=1
		else:
			x, y=randint(0,X_LENGTH-1), randint(0,Y_LENGTH-1)
			if grid[x,y].kind!=KIND_OBSTACLE:
				grid[x,y].kind=KIND_OBSTACLE
				num_obstacles+=1