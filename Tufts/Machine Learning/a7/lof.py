import sys
import math
import numpy
import hashlib

# Load data of the given dimensionality from the file; return a tuple of (datapoints, names) where datapoints is a
# list of the data points and names are the corresponding names (the arrays are parallel). The name of a datapoint is
# assumed to be the last element on the input line.
def load_file(filename, dimensions):
    f = open(filename, 'r')
    while f.readline().strip() != '@data': pass
    # Parse lines into (attributes, name) pairs.
    data = [(numpy.array(map(float, line.strip().split(',')[:dimensions])), line[line.rfind(',') + 1:].strip())
            for line in f.readlines()]
    f.close()
    datapoints, names = zip(*data)
    return numpy.array(datapoints), names

def z_normalize(datapoints):
    mean = numpy.mean(datapoints, axis = 0)
    std_dev = numpy.std(datapoints, axis = 0)
    return numpy.array([(d - mean) / std_dev for d in datapoints])

# When we only care about ranking, i.e. for computing kNN but not outputting the calculated distances, this is faster
# than taking the square root and preserves order.
def euclidean_distance_sq(p1, p2):
    return numpy.sum((p1 - p2) ** 2)

# For when the actual distance value matters. In theory using this function instead of the not square-rooting one 
# should only change the values of the computed LOFs, but not their respective rankings. I use it anyway since
# numerical output is expected and it should be compatible.
def euclidean_distance(p1, p2):
    return math.sqrt(euclidean_distance_sq(p1, p2))

# This can be sped up with a precomputed distance matrix; but it is fast enough on these datasets that I opted
# to use this significantly simpler and clearer definition.
def knn(datapoints, point, k):
    # Ignore the first element, it is point (with distance = 0).
    return numpy.array(sorted(datapoints, key = lambda x: euclidean_distance_sq(point, x))[1:k + 1])

# LOF Functions ---------------------------------------------------------------

def reach_distance(a, x, knn_precomputed):
    return max(knn_precomputed[hashable(x)].k_distance, euclidean_distance(a, x))

def lrd(point, k, knn_precomputed):
    return k / sum(reach_distance(point, n, knn_precomputed) for n in knn_precomputed[hashable(point)].knn)

def lof(datapoints, point, k, knn_precomputed):
    return (sum(lrd(n, k, knn_precomputed) for n in knn_precomputed[hashable(point)].knn) / lrd(point, k, knn_precomputed)) / k

# Threshold is considered the largest jump between two consecutive (when sorted) LOFs. Returns the index of the
# first element after the threshold.
def compute_threshold_index(sorted_lofs):
    # Use infinities: we are unable to compare the jump for the zeroth element; the last element is assumed
    # to be an outlier always.
    return numpy.argmax(numpy.append(sorted_lofs, float('-inf')) - numpy.insert(sorted_lofs, 0, float('inf')))

# Method for making ndarrays hashable to significantly reduce redundant calculations. It doesn't need to be a
# super-clever hash function, it just needs to let the arrays live in a map.
# This is NOT SAFE for the most part, because the dictionary keys (ndarrays) are mutable but changing them
# will not trigger a rehash. As long as we guarantee their contents don't change while they're in the dictionary
# we'll be fine. Once the dictionary is built, everything in it is treated as read-only by the rest of the program.
# http://machineawakening.blogspot.com/2011/03/making-numpy-ndarrays-hashable.html
class hashable:
    def __init__(self, wrapped):
        self.__wrapped = wrapped
        self.__hash = int(hashlib.sha1(wrapped.view(numpy.uint8)).hexdigest(), 16)
    
    def __eq__(self, other):
        return all(self.__wrapped == other.__wrapped)
    
    def __hash__(self):
        return self.__hash
    
    def get(self):
        return numpy.copy(self.__wrapped)
    

# End LOF Functions -----------------------------------------------------------

# Simple struct-like class for holding two fields for precomputed kNN.
class kNNEntry:
    def __init__(self, knn, k_distance):
        self.knn = knn
        self.k_distance = k_distance
    

# Run the LOF algorithm on the given file and print the results to stdout.
def run_lof(filename, dimensions, k, prepend):
    data, names = load_file(filename, dimensions)
    data = z_normalize(data)
    
    data_names = dict(zip(map(lambda x: hashable(x), data), names))
    
    # Make a cache of A -> (kNN(A), k_distance(A)).
    knn_precomputed = {}
    for d in data:
        neighbors = knn(data, d, k)
        knn_precomputed[hashable(d)] = kNNEntry(neighbors, euclidean_distance(neighbors[-1], d))
    
    lof_name_pairs = sorted([(lof(data, d, k, knn_precomputed), data_names[hashable(d)]) for d in data], key = lambda x: x[0])
    
    i = compute_threshold_index(zip(*lof_name_pairs)[0])
    for (score, name) in lof_name_pairs:
        print '%s LOF %s %f %d' % (prepend, name, score, 1 if i > 0 else 0)
        i -= 1

def run_cod(filename, dimensions, k, prepend):
    data, names = load_file(filename, dimensions)
    data = z_normalize(data)
    
    data_names = dict(zip(map(lambda x: hashable(x), data), names))
    
    # Build a (k_distance, datapoint) list and sort it with the highest k_distances at the end.
    k_distance_pairs = sorted([(euclidean_distance(knn(data, d, k)[-1], d), d) for d in data], key = lambda x: x[0])
    i = compute_threshold_index(zip(*k_distance_pairs)[0])
    for (score, d) in k_distance_pairs:
        print '%s COD %s %f %d' % (prepend, data_names[hashable(d)], score, 1 if i > 0 else 0)
        i -= 1


run_lof(sys.argv[1], 35, 25, 'V')
run_lof(sys.argv[2], 12, 5, 'W')

run_cod(sys.argv[1], 35, 25, 'V')
run_cod(sys.argv[2], 12, 5, 'W')
