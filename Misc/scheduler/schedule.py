#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

#using schedule:
#setting (or tuple): NAME=V1[,V2...]
#class:NAME,ROOM,COLOR,DAYS:FROM-TO[,more days...]

#days: MTWRF
#times are in 24-hour, no colon

#examples:
#red=213,13,13
#bkrd_color=white
#Psychology Department,,teal,MW:1500-1700,T:1400-1600,R:1430-1600

#to do:
# fix textsize - there is only one height for each font even for characters as
#  different as 'a' and 'l'
# rounded corners
# smoother fonts somehow?

import fileinput
from PIL import Image, ImageDraw, ImageFont
import ply.lex as lex
import ply.yacc as yacc

classes={}

class Struct:
    pass

class Vector:
    def __init__(self, xy_or_x, y=None):
        if y is None:
            self.x,self.y=xy_or_x
        else:
            self.x=xy_or_x
            self.y=y
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)
    def __mul__(self, scalar):
        #doesn't work as int*vector...
        return Vector(self.x*scalar, self.y*scalar)
    def __neg__(self):
        return Vector(-self.x, -self.y)
    def __eq__(self, other):
        return self.x==other.x and self.y==other.y
    def __getitem__(self, which):
        if which==0:
            return self.x
        elif which==1:
            return self.y
        raise IndexError
    def __setitem__(self, key, value):
        if key==0:
            self.x=value
        elif key==1:
            self.y=value
        raise IndexError
    def __str__(self):
        return 'Vector<%f, %f>' % (self.x, self.y)
    def tuple(self):
        return (self.x, self.y)


colors = {'red' :   (255,0,0),
          'green' : (0,255,0),
          'blue' :  (0,0,255),
          'white' : (255,255,255),
          'black' : (0,0,0)}

variables = ('height', 'day_width', 'spacing', 'x_border', 'y_border', 'header_size',\
             'line_space', 'day_size', 'day_snap', 'class_size', 'class_snap', 'time_size',\
             'time_start_offset', 'time_start_snap', 'time_end_offset', 'time_end_snap',\
             'separator', 'font_folder', 'font', 'font_color', 'bkrd_color', 'filename',\
             'hide_repeats', 'hour_24', 'empty_days')

tokens = ('VARIABLE', 'ASSIGN', 'NUMBER', 'BOOLEAN', 'COMMA', 'COLON', 'DASH', 'STRING', 'DAYS')

def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

t_VARIABLE = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ASSIGN =   r'\s*=\s*'
t_BOOLEAN =  r'([Tt]rue)|([Ff]alse)'
t_COMMA =    r','
t_COLON =    r':'
t_DASH =     r'-'
t_STRING =   r'[-a-zA-Z0-9\\. ]+'
t_DAYS =     r'[MTWRF]+'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


def p_assign_value(p):
    '''assignment : VARIABLE ASSIGN NUMBER
                  | VARIABLE ASSIGN NUMBER COMMA NUMBER COMMA NUMBER
                  | VARIABLE ASSIGN BOOLEAN
                  | VARIABLE ASSIGN STRING'''
    if len(p) == 8:
        exec '%s = (%s, %s, %s)' % (p[1], p[3], p[5], p[7])
    else:
        p[3] = p[3].replace(r'\n', '\n')
        exec '%s = \"%s\"' % (p[1], p[3])

def p_timeblock(p):
    'timeblock : DAYS COLON NUMBER DASH NUMBER'
    s = Struct()
    s.days =  p[1]
    s.start = p[3]
    s.end =   p[5]
    p[0] = s

def p_classinfo(p):
    'classinfo : STRING COMMA STRING COMMA VARIABLE COMMA'
    s = Struct()
    s.name =  p[1]
    s.room =  p[3]
    s.color = p[5]
    p[0] = s

def p_class(p):
    '''class : classinfo timeblock
             | classinfo timeblock COMMA timeblock
             | classinfo timeblock COMMA timeblock COMMA timeblock
             | classinfo timeblock COMMA timeblock COMMA timeblock COMMA timeblock
             | classinfo timeblock COMMA timeblock COMMA timeblock COMMA timeblock COMMA timeblock'''
    c = p[1]
    times = [p[i] for i in xrange(2, len(p), 2)]
    s = Struct()
    if c.name not in classes:
        c.times = times
        classes[c.name] = c


def p_error(p):
    print "Syntax error at '%s'" % p.value


#setup for parsing classes
day_abbr = {'M':'Monday', 'T':'Tuesday', 'W':'Wednesday', 'R':'Thursday', 'F':'Friday'}
schedule = {}
      
#sizing_values
height = 400
day_width = 160
spacing = 1
x_border = 32
y_border = 32
header_size = 40

#font_values
line_space = 1

day_size = 18
day_snap = ''

class_size = 16
class_snap = ''

time_size = 14
time_start_offset = 'left'
time_start_snap = 'left'
time_end_offset = 'left'
time_end_snap = 'left'

#strings
separator = ' - '
font_folder = '/Library/Fonts/'
font = 'MyriadPro-Regular.otf'
font_color = 'black'
bkrd_color = 'white'
filename = 'schedule.png'

#options
hide_repeats = 1
hour_24 = 0
empty_days = 1
        
lex.lex()
yacc.yacc()
for line in fileinput.input():
    yacc.parse(line)

#setup for parsing classes
day_abbr = {'M':'Monday', 'T':'Tuesday', 'W':'Wednesday', 'R':'Thursday', 'F':'Friday'}
schedule = {}

for d in day_abbr:
    schedule[d] = []

#create schedule dictionary in the format DAY:[[NAME, TIMES]...]
for c in classes.values():
    for t in c.times:
        for d in t.days:
            schedule[d].append([c.name, t])

#find earliest and latest timestamps
earliest, latest = 2400, 0
for day in schedule.values():
    for c in day:
        earliest = min(earliest, c[1].start)
        latest = max(latest, c[1].end)

find_length = lambda x, y: (60*(int(y)/100) + y%100) - (60*(int(x)/100) + x%100)

def format_time(time):
    time = int(time)
    string = ''
    if hour_24:
        hour = 24
    else:
        hour = 12
    if time/100 == hour:
        string = '%d' % hour
    else:
        string = '%d' % ((time/100) % hour)
    return string + ':%02d' % (time % 100)

def render_text(block_topleft, block_size, text, font, snaps):
    #returns a dictionary of TOPLEFT:TEXT for rendering
    text = text.split('\n')
    temp = Image.new("RGB", (1,1))
    render = ImageDraw.Draw(img)
    sizes = []
    for t in text:
        sizes.append(draw.textsize(t, font=font))
    width, height = 0, 0
    for (x, y) in sizes:
        height += y + line_space
        width = max(width, x)
    height -= line_space
    
    center = Vector(block_size[0]/2, block_size[1]/2) + Vector(block_topleft)
    
    if snaps[1] == -1:
        y = int(block_topleft[1])
    elif snaps[1] == 0:
        y = int(center[1] - height/2)
    else:
        y = int(block_topleft[1] + block_size[1] - height)
        
    locations = {}
    x = int(block_topleft[0])
    for i in xrange(len(sizes)):
        if snaps[0] == 0:
            x = center[0] - sizes[i][0]/2
        elif snaps[0] == 1:
            x = int(block_topleft[0] + block_size[0] - sizes[i][0])
        locations[(x, y)] = text[i]
        y += sizes[i][1] + line_space
    return locations

def parse_location(string):
    loc = [0,0]
    if 'top' in string:
        loc[1] -= 1
    if 'bot' in string:
        loc[1] += 1
    if 'left' in string:
        loc[0] -= 1
    if 'right' in string:
        loc[0] += 1
    return loc


#pixels per minute
ppm = float(height - header_size) / find_length(earliest, latest)

#setup for drawing to the image
if not empty_days:
    width = 0
    for day_letter in ('M', 'T', 'W', 'R', 'F'):
        if schedule[day_letter]:
            width += day_width + spacing
    width -= spacing
    img = Image.new("RGB", (width + 2*x_border, height + 2*y_border), colors[bkrd_color])
else:
    img = Image.new("RGB", (5*day_width + 4*spacing + 2*x_border, height + 2*y_border), colors[bkrd_color])
draw = ImageDraw.Draw(img)

day_font=ImageFont.truetype(font_folder+font, day_size)
class_font=ImageFont.truetype(font_folder+font, class_size)
time_font=ImageFont.truetype(font_folder+font, time_size)
font_color=colors[font_color]

day_position=Vector(x_border,y_border)
class_position=Vector(x_border,y_border+header_size)
width=day_width+spacing

times_already_drawn=[]

for day_letter in ('M', 'T', 'W', 'R', 'F'):
    if not empty_days and not schedule[day_letter]:
        continue
    #draw day header
    word=render_text(day_position, (day_width, header_size),\
        day_abbr[day_letter], day_font, parse_location(day_snap))
    draw.text(word.keys()[0], day_abbr[day_letter], font=day_font, fill=font_color)
    
    #draw class blocks
    for c in schedule[day_letter]:
        name=c[0]
        start, end=make_int_tuple(c[1].split('-'))
        
        #draw block
        topleft=Vector(class_position[0], find_length(earliest, start)*ppm+class_position[1])
        draw.rectangle((topleft.tuple(), (topleft+Vector(day_width-1, find_length(start, end)*ppm)).tuple()),\
            fill=colors[classes[name][2]])
        
        #draw class name
        if(classes[name][1]):
            string=name+separator+classes[name][1]
        else:
            string=name
        
        lines=render_text(topleft, (day_width, find_length(start, end)*ppm),\
            string, class_font, parse_location(class_snap))
        
        for l in lines:
            draw.text(l, lines[l], font=class_font, fill=font_color)
        
        #draw start timestamp
        if((not hide_repeats) or start not in times_already_drawn):
            size=Vector(draw.textsize(format_time(start), font=time_font))
            offset=parse_location(time_start_offset)
            center=Vector((offset[0]+1)/2.0*day_width+topleft[0], topleft[1])
            time_topleft=center-size
            temp=render_text(time_topleft, size*2, format_time(start), time_font, parse_location(time_start_snap))
            draw.text(temp.keys()[0], temp.values()[0], font=time_font, fill=font_color)
            times_already_drawn.append(start)
        
        #draw end timestamp
        if((not hide_repeats) or end not in times_already_drawn):
            size=Vector(draw.textsize(format_time(end), font=time_font))
            offset=parse_location(time_end_offset)
            center=Vector((offset[0]+1)/2.0*day_width+topleft[0],\
                          find_length(start, end)*ppm+topleft[1])
            time_topleft=center-size
            temp=render_text(time_topleft, size*2, format_time(end), time_font, parse_location(time_end_snap))
            draw.text(temp.keys()[0], temp.values()[0], font=time_font, fill=font_color)
            times_already_drawn.append(end)
    
    day_position.x+=width
    class_position.x+=width

img.save(filename)
