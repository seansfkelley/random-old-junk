from constants import *

class BlockPair:
    def __init__(self, pivot, orbit):
        self.pivot = pivot
        self.orbit = orbit
    
    # Left and right don't avoid counting the pivot or orbit in the can_move check. Fix.
    
    def left(self):
        if self.pivot.can_move_grid(-1, 0) and self.orbit.can_move_grid(-1, 0):
            self.pivot.move_grid(-1, 0)
            self.orbit.move_grid(-1, 0)
    
    def right(self):
        if self.pivot.can_move_grid(1, 0) and self.orbit.can_move_grid(1, 0):
            self.pivot.move_grid(1, 0)
            self.orbit.move_grid(1, 0)
    
    # Against a wall, these rotations should sometimes move the pivot!
    
    def rotate_cw(self):
        if self.orbit.grid_y < self.pivot.grid_y and self.orbit.can_move_grid(1, 1):
            self.orbit.move_grid(1, 1)
        elif self.orbit.grid_x > self.pivot.grid_x and self.orbit.can_move_grid(-1, 1):
            self.orbit.move_grid(-1, 1)
        elif self.orbit.grid_y > self.pivot.grid_y and self.orbit.can_move_grid(-1, -1):
            self.orbit.move_grid(-1, -1)
        elif self.orbit.grid_x < self.pivot.grid_x and self.orbit.can_move_grid(1, -1):
            self.orbit.move_grid(1, -1) 
    
    def rotate_ccw(self):
        if self.orbit.grid_y < self.pivot.grid_y and self.orbit.can_move_grid(-1, 1):
            self.orbit.move_grid(-1, 1)
        elif self.orbit.grid_x > self.pivot.grid_x and self.orbit.can_move_grid(-1, -1):
            self.orbit.move_grid(-1, -1)
        elif self.orbit.grid_y > self.pivot.grid_y and self.orbit.can_move_grid(1, -1):
            self.orbit.move_grid(1, -1)
        elif self.orbit.grid_x < self.pivot.grid_x and self.orbit.can_move_grid(1, 1):
            self.orbit.move_grid(1, 1)
    
    # fall() should do checks to make sure there is space below and also change grid positions.
    
    def fall(self):
        self.pivot.move_sprite(0, DROP_SPEED)
        self.orbit.move_sprite(0, DROP_SPEED)
        
