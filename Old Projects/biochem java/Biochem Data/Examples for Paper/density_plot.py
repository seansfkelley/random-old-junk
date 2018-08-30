# Parameters ------------------------------------------------------------------

# Width is determined by the number of unique x-values. A one-pixel-wide
# column is assigned to each one.
# Later improvement: allow to input a range that each column covers, for x-values.
plot_height = 600

bkrd_color = (255, 255, 255)#(254, 241, 227)
max_density_color = (0, 0, 0)
axis_color = (200, 200, 200)
text_color = (0, 0, 0)

left_border = 50
right_border = 50
top_border = 50
bottom_border = 50
text_v_space = 3
text_h_space = 6

font = '/Users/sk/Library/Fonts/Inconsolata.otf'
font_size = 16

x_axis_label = 'Generations'
y_axis_label = 'Fitness (log base-10 scale)'
title = 'Fitness vs. Generations'
filename = 'Density Plot'

# Generally a float between 1 and 4. 1 means to perform no post-processing to
# each plotted pixel, often making 1-element density pixels difficult to see if
# there exist significantly higher densities elsewhere. 4 about the highest-end
# for plots with some very dense spaces, but sometimes it can make even
# moderately-dense spaces difficult to differentiate from the most dense ones.
dot_color_severity = 2

ignore_threshold = 10

# Implementation --------------------------------------------------------------

import fileinput
from PIL import Image, ImageDraw, ImageFont
from math import log10, fmod, sqrt

generations = {}

min_y, max_y = float('inf'), float('-inf')

format_x = lambda x: int(x)
format_y = lambda y: log10(float(y))

# Read input, dividing it into columns.
num_points = 0
ignored = 0
for line in fileinput.input():
    line = line.strip()
    if len(line) == 0 or line[0] == '#':
        continue
    x, y = line.split(',')
    x, y = format_x(x), format_y(y)

    if x not in generations:
        generations[x] = []
    
    if y > ignore_threshold:
        ignored += 1
        continue
    else:    
        generations[x].append(y)

    min_y = min(min_y, y)
    max_y = max(max_y, y)
    
    num_points += 1

num_gens = max(generations.keys()) + 1
interval = (max_y - min_y) / (plot_height - 1)

max_bucket_size = 0

# Go through each column, placing each data point into the appropriate bucket.
buckets = []
for x in xrange(num_gens):
    buckets.append([0] * plot_height)
    for fitness in generations[x]:
        which_bucket = int((fitness - min_y) / interval)
        buckets[x][which_bucket] += 1
        max_bucket_size = max(max_bucket_size, buckets[x][which_bucket])

max_bucket_size = float(max_bucket_size)

color_diff = (max_density_color[0] - bkrd_color[0],
              max_density_color[1] - bkrd_color[1],
              max_density_color[2] - bkrd_color[2])

def pixel(x):
    x = (x / max_bucket_size) ** (1.0 / dot_color_severity)
    return (int(bkrd_color[0] + color_diff[0] * x),
            int(bkrd_color[1] + color_diff[1] * x),
            int(bkrd_color[2] + color_diff[2] * x))
    # x = int(x * 255.0 / max_bucket_size)
    # return (x, x, x)


# Draw the plot.
img = Image.new('RGB', (left_border + num_gens + right_border, top_border + plot_height + bottom_border), bkrd_color)
for x in xrange(num_gens):
    for y in xrange(plot_height):
        img.putpixel((x + left_border, y + top_border), pixel(buckets[x][plot_height - y - 1]))

# Draw axes and other labelling information.
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(font, font_size)

# Axes.
draw.line((left_border - 1, top_border, 
           left_border - 1, plot_height + top_border, 
           num_gens + left_border, plot_height + top_border,
           num_gens + left_border, top_border,
           left_border - 1, top_border), fill=axis_color)

# Horizontal tick-lines and labels.
tick_interval = 1
# tick_interval = 10 ** (int(log10(max_y - min_y)) - 1)
ppi = plot_height / (max_y - min_y)
tick = round(min_y + tick_interval / 2.0)
tick_y_height = (abs(tick - min_y) * ppi)
while tick < max_y:
    draw.line((left_border - 1, plot_height + top_border - tick_y_height - 1, 
               num_gens + left_border, plot_height + top_border - tick_y_height - 1), 
               fill=axis_color)
    text_size = draw.textsize(str(int(tick)), font=font)
    draw.text((left_border - text_size[0] - text_h_space - 1, 
               plot_height + top_border - tick_y_height - (text_size[1] / 2) - 1), 
               str(int(tick)), font=font, fill=text_color)
    tick += tick_interval
    tick_y_height += ppi

# First-and-last ticks for x-axis.
text_size = draw.textsize('1', font=font)
draw.text((left_border - (text_size[0] / 2) - 1, plot_height + top_border + text_v_space), '1', font=font, fill=text_color)
text_size = draw.textsize(str(num_gens), font=font)
draw.text((left_border + num_gens  - (text_size[0] / 2) - 1, plot_height + top_border + text_v_space), str(num_gens), 
           font=font, fill=text_color)

# Add labels.
text_size = draw.textsize(x_axis_label, font=font)
draw.text((left_border + (num_gens / 2) - (text_size[0] / 2) - 1, plot_height + top_border + text_v_space + text_size[1]),
           x_axis_label, font=font, fill=text_color)

text_size = draw.textsize(y_axis_label, font=font)
temp_img = Image.new('RGB', text_size, bkrd_color)
temp_draw = ImageDraw.Draw(temp_img)
temp_draw.text((0, 0), y_axis_label, font=font, fill=text_color)
temp_img = temp_img.rotate(90, expand=False)
img.paste(temp_img, (left_border - (temp_img.size[0] * 2) - text_h_space - 1,
                     top_border + (plot_height / 2) - (temp_img.size[1] / 2)))

text_size = draw.textsize(title, font=font)
draw.text(((left_border + num_gens + right_border - text_size[0]) / 2, top_border - (text_size[1] * 2)), 
           title, font=font, fill=text_color)

img.save(filename + '.png')

print 'Minimum y: %f; Maximum y: %f\n%d points graphed, maximum density: %d\nIgnored: %d' % (min_y, max_y, num_points, max_bucket_size, ignored)