# this is the most basic A* search - no heap, no tiebreaking, no optimization

def search(self, unit, exceptions=None):
	self.clear()
	self.open.append(unit.current_node)
	self.grid.reset_for_search()
	
	if exceptions:
		for e in exceptions:
			self.grid[e].open=False
	
	for p in unit.path:
		p.solutions.remove(unit)
	
	for x in xrange(X_LENGTH):
		for y in xrange(Y_LENGTH):
			self.grid[x,y].dist_remain=self.distance_estimate((x ,y), unit.goal)
	
	unit.current_node.calc_score()
	
	while True:
		if len(self.open)==0:
			break
		
		best_move=self.open[0]
		
		if best_move==self.grid[unit.goal]:
			break
		
		self.open=self.open[1:]
		self.closed.append(best_move)
		best_move.open=False
		
		for n in self.grid.neighbors_of(best_move):
			if n.open==None:
				n.parent=best_move
				n.open=True
				n.dist_traveled=best_move.dist_traveled+self.movement_cost(n, best_move)
				n.calc_score()
				self.open.append(n)
			elif best_move.dist_traveled+self.movement_cost(n, best_move)<n.dist_traveled:
				n.parent=best_move
				n.dist_traveled=best_move.dist_traveled+self.movement_cost(n, best_move)
				n.calc_score()
		
		self.open.sort(cmp)
	
	solution=[]
	unit.path=[]
	
	if len(self.open)!=0:
		current=self.grid[unit.goal]
		while current:
			solution.append(current)
			current=current.parent
		
		solution.reverse()
		unit.path=solution
		
		# remove nodes in a row that go the same way - but also messes with when obstacles are added
		# to a path after it has been calculated
		# if len(solution)>2:
		# 	unit.path.append(solution[0])
		# 	for i in xrange(1,len(solution)-1):
		# 		if xy_difference(solution[i-1], solution[i])!=xy_difference(solution[i], solution[i+1]):
		# 			unit.path.append(solution[i])
		# else:
		# 		unit.path=solution
	
	for p in unit.path:
		p.solutions.add(unit)