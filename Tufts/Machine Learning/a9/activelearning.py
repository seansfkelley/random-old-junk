import sys
import math
import numpy
import random
import hashlib

# Load data from the given file. The number of dimensions is assumed to be the number of elements on a line, minus one,
# as the last element is assumed to be the class label. Returns a tuple of (datapoints, classes) where datapoints is a
# list of the data points and classes is the corresponding classes list (the lists are parallel).
def load_file(filename):
    f = open(filename, 'r')
    while f.readline().strip() != '@data': pass
    # Parse lines into (attributes, name) pairs.
    data = [(numpy.array(map(float, line.strip().split(',')[:-1])), line[line.rfind(',') + 1:].strip())
            for line in f.readlines()]
    f.close()
    datapoints, labels = zip(*data)
    return numpy.array(datapoints), labels

# When we only care about ranking, i.e. for computing kNN but not outputting the calculated distances, this is faster
# than taking the square root and preserves order.
def distance_sq_curried(p1):
    def f(p2): 
        return numpy.sum((p1 - p2) ** 2)
    return f

def euclidean_distance_sq(p1, p2):
    return numpy.sum((p1 - p2) ** 2)

# This can be sped up with a precomputed distance matrix, but it is fast enough on these datasets that I opted
# to use this significantly simpler and clearer definition. point_in_datapoints correctly adjusts the neighbors
# in the case that the given point is also present in the given datapoints set.
def knn(datapoints, point, k, point_in_datapoints):
    k_plus_one = numpy.array(sorted(datapoints, key = lambda x: euclidean_distance_sq(x, point))[:k + 1])
    if point_in_datapoints:
        # Ignore the first element, it is point (with distance = 0).
        return k_plus_one[1:]
    else:
        return k_plus_one[:k]

# Using all the datapoints in train_datapoints (i.e. assuming they're all considered labeled, and those labels are
# given by the dictionary train_label_dict), compute the classification accuracy for the given k against 
# validate_datapoints and the parallel array validate_labels.
def compute_accuracy(train_datapoints, train_label_dict, validate_datapoints, validate_labels, k):
    correct = 0.0
    for (d, l) in zip(validate_datapoints, validate_labels):
        counts = {}
        # Tally all the votes into counts.
        for c in map(lambda n: train_label_dict[hashable(n)], knn(train_datapoints, d, k, False)):
            counts[c] = counts.get(c, 0) + 1
        # Transform counts into a list to be sorted and pick out the one with the highest votes.
        if sorted(counts.items(), key = lambda x: x[1], reverse = True)[0][0] == l:
            correct += 1
            
    return correct / len(validate_datapoints)
    
# Perform active learning with the given datapoint sets and their respective parallel label lists, m, k, and
# whether or not to select the next m labels using the measure of certainty or randomly.
def active_learning(train_datapoints, train_labels, validate_datapoints, validate_labels, m, k, initial_per_class, prefix = '', certainty_labeling = True):
    train_label_dict = dict(zip(map(lambda x: hashable(x), train_datapoints), train_labels))
    have_labels = numpy.zeros(len(train_datapoints), dtype = numpy.bool)
    
    # Get a unique set of all possible classes.
    classes = set(train_labels)
    
    # Compute which of the items should be labeled initially.
    # First, populate a dictionary with how many more we need of each class.
    labeled_counts = {}
    for l in train_labels:
        if l not in labeled_counts:
            labeled_counts[l] = initial_per_class
    total = initial_per_class * len(labeled_counts)
    
    # Go through the list until all the classes have enough examples that are labeled.
    for (i, d) in enumerate(train_datapoints):
        d = hashable(d)
        for (l, c) in labeled_counts.items():
            if c > 0 and train_label_dict[d] == l:
                have_labels[i] = True
                labeled_counts[l] -= 1
                total -= 1
                break
        if total == 0:
            break
    
    while not numpy.all(have_labels):
        print '%s# labeled = %03d -> accuracy = %.6f' % (prefix, numpy.count_nonzero(have_labels), compute_accuracy(train_datapoints[have_labels], train_label_dict, validate_datapoints, validate_labels, k))
        
        if certainty_labeling:
            certainties = []
            for (i, x) in enumerate(train_datapoints):
                # We could use fancy indexing to pick out only the datapoints that are unlabeled, however, we want
                # i to be correct w/r/t have_labels, which it won't be if we drop intermediate datapoints and 
                # enumerate the remaining set. So we enumerate all the datapoints.
                if have_labels[i]:
                    continue
                # Pick k nearest labeled points.
                neighbors = knn(train_datapoints[have_labels], x, k, True)
                # Compute weighted votes.
                distances_sq = numpy.array(map(distance_sq_curried(x), neighbors))
                variance = numpy.var(numpy.sqrt(distances_sq))
                if variance != 0:
                    votes = numpy.exp(-distances_sq / (2 * variance))
                    vote_labels = numpy.array(map(lambda n: train_label_dict[hashable(n)], neighbors))
                    # Don't actually need to know what the first and second labels are for this example, just how certain they are.
                    label1_vote, label2_vote = sorted((numpy.sum(votes[vote_labels == c]) for c in classes), reverse = True)[:2]
                    # Compute certainty.
                    certainties.append((label1_vote - label2_vote, i))
                else:
                    certainties.append((0, i))
            # Label least certain.
            have_labels[numpy.array(zip(*sorted(certainties))[1][:m])] = True
        else:
            have_labels[random.sample(numpy.nonzero(-have_labels)[0], min(m, numpy.count_nonzero(-have_labels)))] = True
            
    print '%s# labeled = %03d -> accuracy = %.6f' % (prefix, numpy.count_nonzero(have_labels), compute_accuracy(train_datapoints[have_labels], train_label_dict, validate_datapoints, validate_labels, k))
    

# Method for making ndarrays hashable.
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
    


def run_al(train_filename, validate_filename, m, k, initial_per_class, prefix):
    train_data, train_labels = load_file(train_filename)
    
    validate_data, validate_labels = load_file(validate_filename)
    
    active_learning(train_data, train_labels, validate_data, validate_labels, m, k, initial_per_class, prefix)

run_al(sys.argv[1], sys.argv[2], 5, 5, 3, 'twsp: ')
run_al(sys.argv[3], sys.argv[4], 5, 5, 1, 'usps: ')

