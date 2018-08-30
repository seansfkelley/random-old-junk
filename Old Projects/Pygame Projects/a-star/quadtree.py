import math

from astar_constants import *
from random import randint

MIN_SIZE=16

RANDOM_STEPS=36
OBSTACLE_CHANCE=20

class QuadNode:
	def __init__(self, origin, size, pathing=PATH_DEFAULT, parent=None):
		if parent==None and math.modf(math.log(size/MIN_SIZE, 2))[0]!=0:
			raise ValueError('%f invalid size for quadtree based on MIN_SIZE=%d' % (size, MIN_SIZE))
		self.size=int(size)
		self.x, self.y = origin
		self.x_center, self.y_center = self.x+self.size/2, self.y+self.size/2
		self.parent=parent
		self.botleft=self.botright=self.topleft=self.topright=None
		self.pathing=pathing
		self.adjacent={}
		
		self.astar_status=NEW
		self.astar_parent=None
		self.astar_dist_travel=self.astar_dist_remain=self.astar_score=-1
	
	def __str__(self):
		string='QuadNode (%d, %d): %d' % (self.x, self.y, self.size)
		if self.botleft:
			return string+' (split)'
		return string
	
	def __iter__(self):
		if not self.botleft:
			return
		yield self.botleft
		yield self.botright
		yield self.topleft
		yield self.topright
	
	def __contains__(self, other):
		if other is None:
			return False
		return other in (self.botleft, self.botright, self.topleft, self.topright)
	
	def reset_to_leaf(self, pathing):
		# separate variables are used because there is no benefit to grouping - extra work trying to make minor
		# runtime/code size improvements using over-generalizations on only 4 (4!) elements
		all_neighbors=[]
		for child in self:
			all_neighbors+=child.adjacent.keys()
		for n in all_neighbors:
			n.adjacent={}
		self.botleft=self.botright=self.topleft=self.topright=None
		self.pathing=pathing
		self.adjacent={}
	
	def reset_for_search(self):
		if self.botleft:
			for child in self:
				child.reset_for_search()
		else:
			self.astar_status=NEW
			self.astar_parent=None
			self.astar_dist_travel=self.astar_dist_remain=self.astar_score=-1
	
	def split(self):
		if self.size==MIN_SIZE:
			raise ValueError('Cannot downsize minimum-sized node (%d).' % MIN_SIZE)
		for a in self.adjacent:
			a.adjacent={}
		self.botleft=QuadNode((self.x, self.y), self.size/2, self.pathing, self)
		self.botright=QuadNode((self.x_center, self.y), self.size/2, self.pathing, self)
		self.topleft=QuadNode((self.x, self.y_center), self.size/2, self.pathing, self)
		self.topright=QuadNode((self.x_center, self.y_center), self.size/2, self.pathing, self)
		self.adjacent={}
		self.pathing=PATH_VOID # can reliably be used as a has_children flag
	
	def simplify(self):
		"""To be called by a leaf - only recurses upwards. Returns the last node that was condensed."""
		if not self.parent:
			return self
		# one of these is self, if others have children (disallowing simplification), they will have the exclusive PATH_VOID bit
		if self.parent.botleft.pathing==self.parent.botright.pathing==self.parent.topleft.pathing==self.parent.topright.pathing:
			self.parent.reset_to_leaf(self.pathing)
			return self.parent.simplify()
		else:
			return self
	
	def locate(self, x_or_xy, y=None):
		if y==None:
			x,y=x_or_xy
		else:
			x=x_or_xy
		if x<self.x or x>=self.x+self.size or y<self.y or y>=self.y+self.size:
			raise ValueError('Point (%d, %d) out of bounds of %s.' % (x, y, self))
		if self.botleft==None:
			return self
		if x-self.x>=self.size/2:
			if y-self.y>=self.size/2:
				return self.topright.locate(x, y)
			else:
				return self.botright.locate(x, y)
		else:
			if y-self.y>=self.size/2:
				return self.topleft.locate(x, y)
			else:
				return self.botleft.locate(x, y)
	
	def real_distance(self, other):
		# return self.adjacent.get(other, abs(self.x+self.size/2-other.x-other.size/2)+abs(self.y+self.size/2-other.y-other.size/2))
		return self.adjacent.get(other, math.sqrt((self.x_center-other.x_center)**2 +\
													(self.y_center-other.y_center)**2))
	
	def estimated_distance(self, goal):
		return self.real_distance(goal)
	
	def find_adjacent(self, node, force_redo=False):
		"""Should only be called by the root of the tree."""
		if node.adjacent and not force_redo:
			return node.adjacent.keys()
		node.adjacent={}
		
		x, y = node.x-1, node.y
		if x>0:
			while y<node.y+node.size:
				neighbor=self.locate(x, y)
				node.adjacent[neighbor]=node.real_distance(neighbor)
				y+=neighbor.size
		
		x, y = node.x+node.size, node.y
		if x<self.size:
			while y<node.y+node.size:
				neighbor=self.locate(x, y)
				node.adjacent[neighbor]=node.real_distance(neighbor)
				y+=neighbor.size
		
		x, y = node.x, node.y-1
		if y>0:
			while x<node.x+node.size:
				neighbor=self.locate(x, y)
				node.adjacent[neighbor]=node.real_distance(neighbor)
				x+=neighbor.size
		
		x, y = node.x, node.y+node.size
		if y<self.size:
			while x<node.x+node.size:
				neighbor=self.locate(x, y)
				node.adjacent[neighbor]=node.real_distance(neighbor)
				x+=neighbor.size
		
		return node.adjacent.keys()
	


def contact_center(node1, node2):
	if node1.size>node2.size:
		large, small = node1, node2
	else:
		small, large = node1, node2
	
	if abs(slope((large.x_center, large.y_center), (small.x_center, small.y_center))) < 1: #horizontal adjacency
		if small.x<large.x:
			x=small.x+small.size
		else:
			x=large.x+large.size
		y=small.y+small.size/2
	else: # vertical adjacency
		if small.y<large.y:
			y=small.y+small.size
		else:
			y=large.y+large.size
		x=small.x+small.size/2
	
	return (x, y)

	
def randomize(root):
	for i in xrange(RANDOM_STEPS):
		x, y = randint(0, root.size-1), randint(0, root.size-1)
		node=root.locate(x, y)
		if i>3 and randint(1,100)<OBSTACLE_CHANCE:
			node.pathing&=invert_pathing(PATH_WALKABLE)
		else:
			try:
				node.split()
			except ValueError:
				pass
