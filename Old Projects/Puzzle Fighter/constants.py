# Gameplay Attributes
ROWS, COLS = 13, 6

# Apperance Attributes
BLOCK_SIZE = 32
CRASH_FRAMES = 8
CRASH_FPS = 8

# Window Attributes
BORDER_TOP, BORDER_BOTTOM = 100, 100
BORDER_LEFT, BORDER_RIGHT = 100, 100
MIDDLE_SPACING = 100
XRES = BORDER_LEFT + BORDER_RIGHT + MIDDLE_SPACING + 2 * COLS * BLOCK_SIZE
YRES = BORDER_TOP + BORDER_BOTTOM + ROWS * BLOCK_SIZE
DIS_FLAGS = 0

# Internal Attributes
FRAMERATE = 30

DROP_SPEED = 2

# Names
NAME = "Puzzle Fighter"

PREFIX_CRASH = "crash-"
PREFIX_SMALL = "gem-small-"
PREFIX_LARGE = "gem-large-"
IMG_DIR = "images"
IMG_EXT = ".png"
COLORS = ["red", "green", "blue", "yellow"]