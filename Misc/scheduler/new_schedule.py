import fileinput
from PIL import Image, ImageDraw, ImageFont
from euclid import Vector2
import lex.ply as ply
import lex.yacc as yacc

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

class Struct:
    pass

#format: name : Struct of [name, room, color, [days]]
classes = {}

# ('1', '2', '3') -> (1, 2, 3)
make_int_tuple = lambda c: tuple([int(c[i]) for i in xrange(len(c))])

#parse input into classes dictionary
for line in fileinput.input():
    if line[-1] == '\n':
        line = line[:-1]
    temp = line.split('=')
    if len(temp) == 2:
        if temp[0] not in variables:
            try:
                colors[temp[0]] = make_int_tuple(temp[1].split(','))
            except ValueError:
                pass
        else:
            try:
                value = int(temp[1])
            except ValueError:
                value = '\"' + temp[1] + '\"'
            exec '%s = %s' % (temp[0], value)
        continue
    
    temp = line.split(',')
    if len(temp) < 4:
        continue
    if temp[0] not in classes:
        temp[0] = temp[0].replace('\\n', '\n')
        s = Struct()
        s.name =  temp[0]
        s.room =  temp[1]
        s.color = temp[2]
        s.days =  temp[3:]
        classes[temp[0]] = s

#setup for parsing classes
day_abbr = {'M':'Monday', 'T':'Tuesday', 'W':'Wednesday', 'R':'Thursday', 'F':'Friday'}
schedule = {}

for d in day_abbr:
    schedule[d] = []

#create schedule dictionary in the format DAY:[[NAME, START-END]...]
for c in classes.values():
    #format: Struct of name:[name, room, color, [days]]
    #days format: DAYS:FROM-TO
    for times in c.days:
        days, time = times.split(':')
        for d in days:
            s = Struct()
            s.name = c.name
            s.time = time
            schedule[d].append(s)

#find earliest and latest timestamps
earliest, latest = 2400, 0
for day in schedule.values():
    for c in day:
        start, end = make_int_tuple(c.time.split('-'))
        earliest = min(earliest, start)
        latest = max(latest, end)

#length in minutes between early (x) and late (y)
find_length = lambda x, y: (60*(int(y)/100) + y%100) - (60*(int(x)/100) + x%100)

def format_time(time):
    time = int(time)
    string=''
    if hour_24:
        hour = 24
    else:
        hour = 12
    if time / 100 == hour:
        string = '%d' % hour
    else:
        string = '%d' % ((time/100) % hour)
    return string + ':%02d' % (time%100)

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
        height += y+line_space
        width = max(width, x)
    height -= line_space
    
    center = Vector2(block_size[0]/2, block_size[1]/2) + Vector2(block_topleft, 0)
    
    if snaps[1] == -1:
        y = int(block_topleft[1])
    elif snaps[1] == 0:
        y = int(center[1]-height/2)
    else:
        y = int(block_topleft[1]+block_size[1]-height)
        
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
            width += day_width+spacing
    width -= spacing
    img = Image.new("RGB", (width+2*x_border, height+2*y_border), colors[bkrd_color])
else:
    img = Image.new("RGB", (5*day_width+4*spacing+2*x_border, height+2*y_border), colors[bkrd_color])
draw = ImageDraw.Draw(img)

day_font = ImageFont.truetype(font_folder+font, day_size)
class_font = ImageFont.truetype(font_folder+font, class_size)
time_font = ImageFont.truetype(font_folder+font, time_size)
font_color = colors[font_color]

day_position = Vector2(x_border,y_border)
class_position = Vector2(x_border,y_border+header_size)
width = day_width+spacing

times_already_drawn = []

for day_letter in ('M', 'T', 'W', 'R', 'F'):
    if not empty_days and not schedule[day_letter]:
        continue
    
    #draw day header
    word = render_text(day_position, (day_width, header_size),\
                       day_abbr[day_letter], day_font, parse_location(day_snap))
    draw.text(word.keys()[0], day_abbr[day_letter], font=day_font, fill=font_color)
    
    #draw class blocks
    for c in schedule[day_letter]:
        name = c.name
        start, end = make_int_tuple(c.time.split('-'))
        
        #draw block
        topleft = Vector2(class_position[0], find_length(earliest, start)*ppm + class_position[1])
        draw.rectangle((topleft.tuple(), (topleft+Vector2(day_width-1, find_length(start, end)*ppm)).tuple()),\
                       fill=colors[classes[name][2]])
        
        #draw class name
        if(classes[name].room):
            string = name + separator + classes[name].room
        else:
            string = name
        
        lines = render_text(topleft, (day_width, find_length(start, end)*ppm),\
                            string, class_font, parse_location(class_snap))
        
        for l in lines:
            draw.text(l, lines[l], font=class_font, fill=font_color)
        
        #draw start timestamp
        if((not hide_repeats) or start not in times_already_drawn):
            size=Vector2(draw.textsize(format_time(start), font=time_font))
            offset=parse_location(time_start_offset)
            center=Vector2((offset[0]+1)/2.0*day_width+topleft[0], topleft[1])
            time_topleft=center-size
            temp=render_text(time_topleft, size*2, format_time(start), time_font, parse_location(time_start_snap))
            draw.text(temp.keys()[0], temp.values()[0], font=time_font, fill=font_color)
            times_already_drawn.append(start)
        
        #draw end timestamp
        if((not hide_repeats) or end not in times_already_drawn):
            size=Vector2(draw.textsize(format_time(end), font=time_font))
            offset=parse_location(time_end_offset)
            center=Vector2((offset[0]+1)/2.0*day_width+topleft[0],\
                          find_length(start, end)*ppm+topleft[1])
            time_topleft=center-size
            temp=render_text(time_topleft, size*2, format_time(end), time_font, parse_location(time_end_snap))
            draw.text(temp.keys()[0], temp.values()[0], font=time_font, fill=font_color)
            times_already_drawn.append(end)
    
    day_position.x += width
    class_position.x += width

img.save(filename)