import os
import os.path
import shutil
import sys
import getopt

SRC_DIR='/Users/sk/Downloads/'
DST_DIR='/Users/sk/Downloads/'
PROG_NAME=''
FILE_TYPE=''
OVERWRITE=False

opts=getopt.getopt(sys.argv[1:], 's:d:a:t:o', 
				['source=', 'destination=', 'application=', 'type=', 'overwrite'])[0]

for (option, argument) in opts:
	option=option.lstrip('-')
	if option[0]=='s':	
		SRC_DIR=argument
	elif option[0]=='d':
		DST_DIR=argument
	elif option[0]=='a':
		PROG_NAME=argument
	elif option[0]=='t':
		if argument[0] != '.':
			argument = '.'+argument
		FILE_TYPE=argument
	elif option[0]=='o':
		OVERWRITE=True

files=filter(lambda x: os.path.splitext(x)[1]==FILE_TYPE, os.listdir(SRC_DIR))

if not files:
	sys.exit()

for f in files:
	if os.path.exists(os.path.join(DST_DIR, f)):
		if OVERWRITE:
			os.remove(os.path.join(DST_DIR, f))
		else:
			continue

	shutil.move(os.path.join(SRC_DIR, f), os.path.join(DST_DIR, f))
	if PROG_NAME:
		if os.fork() == 0:
			os.execvp('open', ['open', PROG_NAME, os.path.join(DST_DIR, f)])