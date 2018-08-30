import sys
import math

def distance(v1, v2, dim):
    return math.sqrt(sum([(v1[i] - v2[i]) ** 2 for i in xrange(dim)]))


def z_normalize(data):
    dimensions = xrange(len(data[0]))
    # Sum all vectors in data with reduce, then average the sum vector with map.
    mean = map(lambda x: x / len(data), reduce(lambda x, y: [x[i] + y[i] for i in dimensions], data))
    # Mirror data by creating a list replacing each element with its squared error.
    sq_error = [[(d[i] - mean[i]) ** 2 for i in dimensions] for d in data]
    # Compute standard deviations from squared errors.
    std_dev = map(lambda x: math.sqrt(x / (len(data) - 1)), reduce(lambda x, y: [x[i] + y[i] for i in dimensions], sq_error))
    # Compute normalized values.
    return map(lambda x: [(x[i] - mean[i]) / std_dev[i] for i in dimensions], data)


f = open(sys.argv[1], 'r')
while f.readline() != '@data\n': pass

train_data = []
train_data_classes = []
for line in f.readlines():
    d = line.strip().split(',')
    train_data.append(map(float, d[:13]))
    train_data_classes.append(int(d[13]))

train_data = z_normalize(train_data)

train_data = [train_data[i] + [train_data_classes[i]] for i in xrange(len(train_data))]

f.close()

accuracies = []
for k in xrange(1, 22, 2):
    correct = 0.0
    for i in xrange(len(train_data)):
        left_out = train_data[i]
        # Sort by distance, keep only k nearest.
        knn = sorted(train_data, key = lambda x: distance(left_out, x, 13))[1:k+1]
        # Transform each neighbor to a condensed (distance, species) tuple.
        knn = map(lambda x: (distance(left_out, x, 13), x[13]), knn)
        # Combine all neighbors of the same type into (total distance, species, count) tuples (one for each species).
        knn = [reduce(lambda x, y: (x[0] + y[0], wine, x[2] + 1), filter(lambda x: x[1] == wine, knn), [0, wine, 0]) for wine in (1, 2, 3)]
        # Filter out species with no neighbors, then sort with primary key count and secondary key total distance.
        knn = sorted(sorted(filter(lambda x: x[2] > 0, knn), key = lambda x: x[0]), key = lambda x: x[2], reverse = True)
        if knn[0][1] == left_out[13]: correct += 1
    accuracies.append((k, correct / len(train_data)))
print accuracies
        