import os
import os.path
import shutil
import sys
import getopt

SRC_DIR='/Users/sk/Downloads/'
DST_DIR='/Users/sk/Documents/Crosswords/'
PROG_NAME='/Applications/Across Lite v2.0'

opts=getopt.getopt(sys.argv[1:], 's:d:a:', ['source=', 'destination=', 'application='])[0]

for (option, argument) in opts:
	option=option.lstrip('-')
	if option[0]=='s':	
		SRC_DIR=argument
	elif option[0]=='d':
		DST_DIR=argument
	elif option[0]=='a':
		PROG_NAME=argument

puzzles=filter(lambda x: os.path.splitext(x)[1]=='.puz', os.listdir(SRC_DIR))

if not puzzles:
	sys.exit()

for p in puzzles:
	if os.path.exists(os.path.join(DST_DIR, p)):
		os.remove(os.path.join(SRC_DIR, p))
	else:
		shutil.move(os.path.join(SRC_DIR, p), os.path.join(DST_DIR, p))

os.execvp('open', ['open', PROG_NAME, os.path.join(DST_DIR, puzzles[0])])