NEW, OPEN, CLOSED = 0, 1, 2

CROSS_PRODUCT_FACTOR=.1

# bitmask constants for pathing
PATH_VOID=      1
PATH_WALKABLE=	2
PATH_SWIMMABLE=	4
PATH_FLYABLE=	8
PATH_BUILDABLE=	16

PATH_ALL=		31

PATH_DEFAULT=PATH_WALKABLE|PATH_FLYABLE|PATH_BUILDABLE

def invert_pathing(p):
	return PATH_ALL^p

def bin(x):
	return ''.join(x & (1 << i) and '1' or '0' for i in xrange(7,-1,-1))

def slope(xy0, xy1):
	if xy1[0]==xy0[0]:
		return float('nan')
	return float(xy1[1]-xy0[1])/(xy1[0]-xy0[0])
