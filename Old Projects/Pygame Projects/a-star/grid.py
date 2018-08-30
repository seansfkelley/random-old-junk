from constants import *

class GridSquare:
	def __init__(self):
		#run-immutable traits
		self.kind=KIND_NORMAL
		self.indices=None
		self.solutions=pygame.sprite.Group()
		self.occupants=pygame.sprite.Group()
		
		#run-mutable traits
		self.reset_for_search()
	
	def __getitem__(self, index):
		return self.indices[index]
	
	def __cmp__(self, other):
		if not isinstance(other, GridSquare):
			return False
		return self.score-other.score
		
	def __str__(self):
		return 'Node<%d,%d>: %d occ' % (self[0], self[1], len(self.occupants))
	
	def calc_score(self):
		self.score=self.dist_traveled+self.dist_remain
	
	def reset_for_search(self):
		self.parent=None
		self.score=self.dist_traveled=self.dist_remain=0
		self.open=None

class Grid:
	def __init__(self):
		self.grid=[[GridSquare() for i in xrange(Y_LENGTH)] for j in xrange(X_LENGTH)]
		
		for x in xrange(X_LENGTH):
			for y in xrange(Y_LENGTH):
				self.grid[x][y].indices=(x,y)
	
	def __getitem__(self, xy):
		try:
			xy[0]
			return self.grid[xy[0]][xy[1]]
		except TypeError:
			return self.grid[xy]
	
	def __iter__(self):
		for x in xrange(X_LENGTH):
			for y in xrange(Y_LENGTH):
				yield self.grid[x][y]
	
	def obstacle_in_range(self, x, y, radius):
		if self[x,y].kind==KIND_OBSTACLE:
			return True
		
		if radius==0:
			return False
		
		x_coord, y_coord = indices_to_centered_coords((x,y))
		if x_coord<radius or y_coord<radius or (Y_RESOLUTION-y_coord)<radius or (X_RESOLUTION-x_coord)<radius:
			return True
		
		# stunningly inefficient and doesn't test a pretty circle with large grid sizes (use midpoint algorithm later?)
		grid_radius=int(radius/GRID_SIZE+.5) # equivalent to rounding
		grid_radius_sq=grid_radius**2
		for test_x in xrange(x-grid_radius, x+grid_radius+1):
			for test_y in xrange(y-grid_radius, y+grid_radius+1):
				if (x-test_x)**2 + (y-test_y)**2 < grid_radius_sq and self[test_x, test_y].kind==KIND_OBSTACLE:
					return True
		
		return False
		
	
	def neighbors_of(self, node, collision_radius=0):
		
		# including diagonals, disallowing diagonal moves over orthagonal obstacles
		# neighbors=[]
		# orthagonal=[(0,1), (1,0), (0, -1), (-1, 0)]
		# diagonal=[(-1,1), (1,1), (1,-1), (-1,-1)]
		# node_x,node_y=node.indices
		# 
		# for (x,y) in orthagonal:
		# 	x,y=x+node_x,y+node_y
		# 	if x<0 or y<0 or x>=X_LENGTH or y>=Y_LENGTH or self[x,y].open==False:
		# 		continue
		# 	#remove diagonals that border obstacles, that movement doesn't make sense
		# 	if self[x,y].kind==KIND_OBSTACLE:
		# 		i=0
		# 		while i<len(diagonal):
		# 			if diagonal[i][0]+node_x==x or diagonal[i][1]+node_y==y:
		# 				del diagonal[i]
		# 			else:
		# 				i+=1
		# 		continue
		# 	neighbors.append(self[x,y])
		# 
		# for (x,y) in diagonal:
		# 	x,y=x+node_x,y+node_y
		# 	if x<0 or y<0 or x>=X_LENGTH or y>=Y_LENGTH or self[x,y].open==False or self[x,y].kind==KIND_OBSTACLE:
		# 		continue
		# 	neighbors.append(self[x,y])
		# 	
		# return neighbors
		
		node_x,node_y=node.indices
		neighbors=[]
		for (x, y) in ((0,1), (1,0), (0, -1), (-1, 0)):
			x,y=x+node_x,y+node_y
			if x<0 or y<0 or x>=X_LENGTH or y>=Y_LENGTH or self[x,y].open==False or self.obstacle_in_range(x, y, collision_radius):
				continue
			neighbors.append(self[x,y])
		return neighbors
	
	def reset_for_search(self):
		for x in xrange(X_LENGTH):
			for y in xrange(Y_LENGTH):
				self.grid[x][y].reset_for_search()
	

