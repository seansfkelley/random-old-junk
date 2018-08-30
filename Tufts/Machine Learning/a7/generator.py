import math
import numpy
import random
import sys

# Generate clusters + outliers, given a number of dimensions and examples. The number of clusters is chosen randomly
# based on this information.

# Method: 
# produce some number of cluster centers (see below)
# repeat #examples times:
#   if random() > chance_of_generating_outlier:
#     generate a point in a normal distribution around a randomly-selected center
#   else:
#     generate an outlier with random values for all its attributes

OUTLIER_PCT = 0.1

example_count = -1

def generate_example(center):
    global example_count
    example_count += 1
    if random.random() > OUTLIER_PCT:
        # Generate some in-cluster data point.
        return list(center + numpy.random.normal(0, 1, (g_dims,))) + ['ex%d' % example_count]
    # Generate and outlier.
    return list(numpy.random.random(g_dims) * 25) + ['ol%d' % example_count]

if len(sys.argv) < 4:
    'usage: %s num-example num-dimensions output-filename' % sys.argv[0]

g_dims = int(sys.argv[2])

f= open(sys.argv[3], 'w')

f.write('@data\n')

# Generate some random number of clusters (based on how many data points we have) for the outliers to be away from.
centers = [numpy.random.random(g_dims) * 25 for i in xrange(int((0.5 + random.random() / 2) * int(sys.argv[1]) / 20))]

for i in xrange(int(sys.argv[1])):
   f.write(','.join(map(str, generate_example(random.choice(centers)))) + '\n')

f.close()