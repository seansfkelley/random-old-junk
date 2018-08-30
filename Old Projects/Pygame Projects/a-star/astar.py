from astar_constants import *

class AStarSearch:
	def __init__(self, map):
		self.map=map
		self.reset()
	
	def reset(self):
		self.open=[]
		self.map.reset_for_search()
	
	def search(self, start_coords, end_coords, pathing_type, exceptions=None):
		start=self.map.locate(start_coords)
		end=self.map.locate(end_coords)
		
		self.reset()
		self.open.append(start)
		
		if exceptions:
			for e in exceptions:
				self.map.astar_status=CLOSED
		
		start.astar_dist_travel=0
		start.astar_dist_remain=start.estimated_distance(end)
		start.astar_score=start.astar_dist_remain+start.astar_dist_travel
		
		astar_checks=0
		
		# main A* search loop
		
		while True:
			if len(self.open)==0:
				break
			
			best_move=self.open[0]
			
			if best_move==end:
				break
			
			self.open=self.open[1:]
			best_move.astar_status=CLOSED
			
			for n in self.map.find_adjacent(best_move):
				if n.astar_status==CLOSED or not n.pathing&pathing_type:
					continue
				elif n.astar_status==NEW:
					n.astar_parent=best_move
					n.astar_status=OPEN
					n.astar_dist_travel=best_move.astar_dist_travel+best_move.real_distance(n)
					n.astar_score=n.astar_dist_remain+n.astar_dist_travel
					self.open.append(n)
				elif best_move.astar_dist_travel+best_move.adjacent[n]<n.astar_dist_travel:
					n.astar_parent=best_move
					n.astar_dist_travel=best_move.astar_dist_travel+best_move.real_distance(n)
					n.astar_score=n.astar_dist_remain+n.astar_dist_travel
				astar_checks+=1
			
			self.open.sort(lambda x, y: int(x.astar_score-y.astar_score))
		
		# begin post-processing of the path
		
		solution=[]
		
		if len(self.open)!=0:
			current=end
			while current:
				solution.append(current)
				current=current.astar_parent
			solution.reverse()
		
		print 'A* checked %d nodes' % astar_checks
		
		return solution
	
