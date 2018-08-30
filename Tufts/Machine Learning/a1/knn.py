import sys
import math

def distance(v1, v2, dim):
    return math.sqrt(sum([(v1[i] - v2[i]) ** 2 for i in xrange(dim)]))


f = open(sys.argv[1], 'r')
while f.readline() != '@data\n': pass

train_data = []
for line in f.readlines():
    d = line.strip().split(',')
    d = map(float, d[:4]) + d[4:]
    train_data.append(d)

f.close()


f = open(sys.argv[2], 'r')
while f.readline() != '@data\n': pass

output = open(sys.argv[3], 'w')

for line in f.readlines():
    candidate = line.strip().split(',')
    candidate = map(float, candidate[:4]) + candidate[4:]
    output_line = line.strip()
    for k in xrange(1, 10, 2):
        # Sort by distance, keep only k nearest.
        knn = sorted(train_data, key = lambda x: distance(candidate, x, 4))[:k]
        # Transform each neighbor to a condensed (distance, species) tuple.
        knn = map(lambda x: (distance(candidate, x, 4), x[4]), knn)
        # Combine all neighbors of the same type into (total distance, species, count) tuples (one for each species).
        knn = [reduce(lambda x, y: (x[0] + y[0], iris, x[2] + 1), filter(lambda x: x[1] == iris, knn), [0, iris, 0]) for iris in ['versicolor', 'virginica', 'setosa']]
        # Filter out species with no neighbors, then sort with primary key count and secondary key total distance.
        knn = sorted(sorted(filter(lambda x: x[2] > 0, knn), key = lambda x: x[0]), key = lambda x: x[2], reverse = True)
        output_line += ',' + knn[0][1]
    output.write(output_line + '\n')
    
f.close()
output.close()