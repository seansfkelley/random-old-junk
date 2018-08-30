import numpy
import random
import sys

def euclidean_distance_sq(p1, p2):
    return numpy.sum((p1 - p2) ** 2)

def z_normalize(datapoints):
    mean = numpy.mean(datapoints, axis = 0)
    std_dev = numpy.std(datapoints, axis = 0)
    std_dev[std_dev == numpy.zeros(len(std_dev))] = 1
    return numpy.array([(d - mean) / std_dev for d in datapoints])

def compute_assignments(centers, datapoints):
    clusters =[list() for i in xrange(len(centers))]
    for point in datapoints:
        closest, closest_distance = None, float('inf')
        for i in xrange(len(centers)):
            d = euclidean_distance_sq(point, centers[i])
            if d < closest_distance:
                closest, closest_distance = i, d
        clusters[closest].append(point)
    for i in xrange(len(centers)):
        clusters[i] = numpy.array(clusters[i])
    return clusters

def compute_centers(clusters):
    return [numpy.mean(c, axis = 0) for c in clusters]

def clusterings_identical(clusters1, clusters2):
    for (c1, c2) in zip(clusters1, clusters2):
        if len(c1) != len(c2):
            return False
        for (d1, d2) in zip(c1, c2):
            if not all(d1 == d2):
                return False
    return True

def kmeans(initial_centers, datapoints):
    old_clusters = None
    centers = initial_centers
    for i in xrange(50):
        clusters = compute_assignments(centers, datapoints)
        centers = compute_centers(clusters)
        if old_clusters and clusterings_identical(old_clusters, clusters):
            break
        old_clusters = clusters
    return clusters

def random_points(datapoints, k):
    return random.sample(datapoints, k)

def sum_sq_err(clusters):
    total = 0
    centers = compute_centers(clusters)
    for i in xrange(len(clusters)):
        for point in clusters[i]:
            total += euclidean_distance_sq(centers[i], point)
    return total

class hashable:
    def __init__(self, wrapped):
        self.__wrapped = wrapped
        self.__hash = int(hashlib.sha1(wrapped.view(numpy.uint8)).hexdigest(), 16)

    def __eq__(self, other):
        return all(self.__wrapped == other.__wrapped)

    def __hash__(self):
        return self.__hash

def load_file(filename, dimensions):
    f = open(filename, 'r')
    while f.readline().strip() != '@data': pass
    # Parse lines into (attributes, name) pairs.
    data = [(numpy.array(map(float, line.strip().split(',')[:dimensions])), line[line.rfind(',') + 1:].strip())
            for line in f.readlines()]
    f.close()
    datapoints, names = zip(*data)
    return numpy.array(datapoints)

norm_data = z_normalize(load_file(sys.argv[1], 19))

for k in xrange(1, 13):
    print sum(sum_sq_err(kmeans(random_points(norm_data, k), norm_data)) for i in xrange(5)) / 5.0,
    sys.stdout.flush()

