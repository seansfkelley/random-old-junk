import sys
import math

# The array module is extremely useful for keeping memory usage reasonable. Normal Python lists have to store much more
# than regular arrays because of their nonhomogeneity and ability to store objects (I think because primitives are 
# generally represented as objects in the system). Using arrays for the key memoization data reduced memory usage by
# 80%.
import array

# Return a list of (k, classification accuracy) tuples for the data points listed in class_list using the k values given
# by the iterable ks. class_list is simply a list of class instances, whose valid values are listed in the iterable
# valid_classes. Critically, the order of class instances in class_list corresponds to the order of distances that have
# been precomputed and stored in distance_matrix (described in http://en.wikipedia.org/wiki/Distance_matrix). 
def knn_loocv(class_list, distance_matrix, ks, valid_classes):
    accuracies = []
    for k in ks:
        correct = 0.0
        # class_list[i] is the left-out element.
        for i in xrange(len(class_list)):
            # Zip together into list of corresponding (distance, class) tuples for each element, then sort by distance.
            # Drop all but the k closest elements (but drop the first element, since it will be the left-out element
            # as distance(x, x) = 0).
            # This sorting takes up about 50% of the total runtime; the key function itself uses about 10%.
            knn = sorted(zip(distance_matrix[i], class_list), key = lambda x: x[0])[1:k + 1]
            # Combine all neighbors of the same type into (total distance, class, count) tuples (one for each class).
            knn = [reduce(lambda x, y: (x[0] + y[0], c, x[2] + 1), filter(lambda x: x[1] == c, knn), [0, c, 0]) for c in valid_classes]
            # Sort with primary key count and secondary key total distance (sorted() is guaranteed stable).
            knn = sorted(sorted(knn, key = lambda x: x[0]), key = lambda x: x[2], reverse = True)
            # Verify most votes against the supplied classification.
            if knn[0][1] == class_list[i]: correct += 1
        accuracies.append((k, correct / len(class_list)))
    return accuracies

# Takes a list of numeric vectors and returns a z-normalized list of vectors in the same order as the input. Each element
# at some index i of each vector is normalized with respect to the elements at the same index i of each other vector. The 
# vectors are assumed to all be the same length.
def z_normalize(data):
    dimensions = xrange(len(data[0]))
    # Sum all vectors in data with reduce, then average the sum vector with map.
    mean = map(lambda x: x / len(data), reduce(lambda x, y: [x[i] + y[i] for i in dimensions], data))
    # Mirror data by creating a list replacing each element with its squared error.
    sq_error = [[(d[i] - mean[i]) ** 2 for i in dimensions] for d in data]
    # Compute standard deviations from squared errors.
    std_dev = map(lambda x: math.sqrt(x / (len(data) - 1)), reduce(lambda x, y: [x[i] + y[i] for i in dimensions], sq_error))
    # Compute normalized values.
    norm = map(lambda x: [(x[i] - mean[i]) / std_dev[i] for i in dimensions], data)
    return [array.array('f', n) for n in norm]

# Computes pairwise distances for each vector in the list data based on the given 2-parameter distance function. Returns
# distance matrix as described in http://en.wikipedia.org/wiki/Distance_matrix.
def distance_matrix(data, distance):
    # Compute a 0-padded upper triangular matrix of distances.
    distance_upper_tri = [[0.0] * i + [distance(data[i], data[j]) for j in xrange(i, len(data))] for i in xrange(len(data))]
    # Convert upper triangular matrix into a full matrix (reflect across diagonal) to make accessing one element's distances easier.
    distance_matrix = [([distance_upper_tri[j][i] for j in xrange(i)] + distance_upper_tri[i][i:len(data)]) for i in xrange(len(data))]
    return [array.array('f', d) for d in distance_matrix]

# Computes the sum of the two matrices, assuming they are the same dimensions.
def sum_matrices(m1, m2):
    # This function takes up about 20-25% of the total runtime.
    rows, cols = xrange(len(m1)), xrange(len(m1[0]))
    return [array.array('f', [m1[i][j] + m2[i][j] for j in cols]) for i in rows]

# Part 2 ----------------------------------------------------------------------
f = open(sys.argv[1], 'r')
while f.readline() != '@data\n': pass

loocv_data = []
loocv_data_classes = []
for line in f.readlines():
    d = line.strip().split(',')
    loocv_data.append(map(float, d[:13]))
    loocv_data_classes.append(int(d[13]))

f.close()

norm_loocv_data = z_normalize(loocv_data)

# Compute squared Euclidian distance between two vectors (assumed to contain only numeric elements).
def euclid_distance_sq(v1, v2):
    # Don't use sqrt: we only care about ordering, not exact numerical accuracy for distances.
    return sum([(v1[i] - v2[i]) ** 2 for i in xrange(len(v1))])

f = open(sys.argv[2], 'w')

f.write('with normalized data\n')
f.writelines(map(lambda x: 'k = %2d: accuracy = %.6f\n' % x, knn_loocv(loocv_data_classes, distance_matrix(norm_loocv_data, euclid_distance_sq), xrange(1, 22, 2), (1, 2, 3))))
f.write('\nwith unnormalized data\n')
f.writelines(map(lambda x: 'k = %2d: accuracy = %.6f\n' % x, knn_loocv(loocv_data_classes, distance_matrix(loocv_data, euclid_distance_sq), xrange(1, 22, 2), (1, 2, 3))))

f.close()

# Part 3 ----------------------------------------------------------------------
f = open(sys.argv[3], 'r')
while f.readline() != '@data\n': pass

car_data_all = []
car_data_classes = []
for line in f.readlines():
    d = line.strip().split(',')
    car_data_all.append(map(float, d[:36]) + [0.0 if d[36] == 'noncar' else 1.0])
    car_data_classes.append(car_data_all[-1][36])

f.close()

# Filter Method ---------------------------------------------------------------

# Takes a list of z-normalized numeric vectors and returns a list of absolute values of PCCs. The ith element 
# represents the correlation of all the elements in the input vectors in the ith position with respect to the 
# elements at index wrt_index. The  element at wrt_index in the result is 1. The method used is described here:
# http://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient#Definition
def pcc(data, wrt_index):
    # Reuse the z-score function to compute the terms in the summation.
    r = [map(lambda x: x * data[i][wrt_index], data[i]) for i in xrange(len(data))]
    # Perform summation (vector addition) and divide by n - 1 to yield all 36 PCCs.
    r = map(lambda x: x / (len(data) - 1), reduce(lambda x, y: [x[i] + y[i] for i in xrange(len(data[0]))], r))
    # Should be one, but machine error frequently causes it to be off by negligible amounts. We should guarantee
    # that it is one.
    r[wrt_index] = 1.0
    return array.array('f', map(abs, r))

norm_car_data_all = z_normalize(car_data_all)

r = pcc(norm_car_data_all, 36)[:36]
# We don't want the class variable to be incorporated into the knn calculations.
norm_car_data = [d[:36] for d in norm_car_data_all]

f = open(sys.argv[4], 'w')

f.write('correlations\n')

r_descending = sorted(zip(r, xrange(36)), key = lambda x: x[0], reverse = True)
for (r_value, i) in r_descending:
    f.write('f%02d: %.6f\n' % (i, r_value))

# print 'Precomputing distance matrices...',
# sys.stdout.flush()

# Compute the one-feature pairwise distances. Because we don't use square root for distances, these can be simply added
# together in any order to produce a distance matrix for whatever combination of features we want to use. This giant
# list of matrices consumes nearly all the memory used by the program.
feature_distances = [distance_matrix(norm_car_data, lambda x, y: (x[i] - y[i]) ** 2) for i in xrange(36)]

# print 'done'

f.write('\naccuracies\n')

feature_indices = zip(*r_descending)[1]
# Minimize the number of matrix additions we need by keeping track of the most recently used matrix in a cumulative
# variable.
current_distance_matrix = [[0] * len(norm_car_data) for i in xrange(len(norm_car_data))]
for m in xrange(36):
    current_distance_matrix = sum_matrices(current_distance_matrix, feature_distances[feature_indices[m]])
    f.write('m = %2d: accuracy = %.6f\n' % (m + 1, knn_loocv(car_data_classes, current_distance_matrix, (7,), (0, 1))[0][1]))

f.close()

# Wrapper Method --------------------------------------------------------------

f = open(sys.argv[5], 'w')

current_feature_set, accuracies = [], []
candidate_feature_set = range(36)
previous_accuracy = 0

current_distance_matrix = [[0] * len(norm_car_data) for i in xrange(len(norm_car_data))]

# This while loop's termination condition does not accurately represent the normal termination condition:
# that of not having increasing accuracy. This is done with a break in the body of loop, in order to avoid
# ugly workarounds with extra variables and unnecessarily breaking up the different parts of the loop-update
# logic between the beginning and end of the loop.
# This minimizes computation by culmulatively summing the matrices as the corresopnding features are incorporated
# into the accepted feature set. This works because our measure, Euclidean distance squared, is a monotonically
# increasing function and we only care about ranking, not exact value.
# Produces two parallel lists in current_feature_set and accuracies. The last item in eash list is the lst best-
# performing feature having an accuracy below that of the previous -- the termination condition.
while len(candidate_feature_set) > 0:
    # print 'Checking new candidate features with fixed feature set ' + str(current_feature_set) + ' (accuracy %.6f):' % previous_accuracy, 
    # sys.stdout.flush()
    scores = []
    for feature in candidate_feature_set:
        # print f,
        # sys.stdout.flush()
        scores.append((feature, knn_loocv(car_data_classes, sum_matrices(current_distance_matrix, feature_distances[feature]), (7,), (0, 1))[0][1]))
    # print
    best_feature, current_accuracy = sorted(scores, key = lambda x: x[1], reverse = True)[0]
    
    accuracies.append(current_accuracy)
    current_feature_set.append(best_feature)
    candidate_feature_set.remove(best_feature)
    
    f.write(str(current_feature_set) + '\naccuracy = %.6f\n' % current_accuracy)
    
    if current_accuracy <= previous_accuracy:
        # print 'Terminating: best feature %d lowers accuracy to %.6f' % (best_feature, current_accuracy)
        break
    previous_accuracy = current_accuracy
    
    current_distance_matrix = sum_matrices(current_distance_matrix, feature_distances[best_feature])

f.close()

# print 'Selected feature set: %s\nAccuracies: %s' % (str(current_feature_set), str(accuracies))

# Hybrid Method ---------------------------------------------------------------

# Takes a list of candidate features that can be selected, and computes which is the most likely to improve performance
# by calculating it's "usefulness": a heuristic that grades how each feature might perform by facotring in its 
# correlation with the currently selected features as well as with the class variable. The last row and column in rs are
# assumed to represent the class variable. Returns the element from the candidate_feature_set that represents the most 
# useful feature. When the current feature set is empty, the feature that best correlates with the class variable is 
# chosen.
def best_feature(current_feature_set, candidate_feature_set, rs):
    if len(current_feature_set) == 0:
        return rs[-1].index(max(rs[-1][:-1]))
    
    # Heuristic 1: Sum correlations with respect to currently selected features, multiply by correlation with class.
    # This heuristic actually favors features correlated with the currently selected features.
    # candidate_scores = [(candidate, sum([rs[candidate][f] for f in current_feature_set]) * rs[candidate][-1]) for candidate in candidate_feature_set]
    
    # Heuristic 2: Sum (1 - correlations) with respect to currently selected features, multiply by correlation with class.
    # This heuristic is like the previous except that it favors features with lower correlations to the currently
    # selected feature set. I expected it to perform better than the previous, but it actually performs worse!
    # candidate_scores = [(candidate, sum([1 - rs[candidate][f] for f in current_feature_set]) * rs[candidate][-1]) for candidate in candidate_feature_set]
    
    # Heuristic 3: Multiply correlations with respect to currently selected features and class variable.
    # Again, counter to my intuition, the variant where this favors low correlation with selected features performs
    # worse than this version, which should be in favor of those correlated with the selected features.
    # This heuristic may underflow with lots of features.
    # candidate_scores = [(candidate, reduce(lambda x, y: x * y, [rs[candidate][f] for f in current_feature_set], rs[candidate][-1])) for candidate in candidate_feature_set]
    
    # Heuristic 4: Add the logs of the correlations with respect to the selected features, plus 1 (to keep log > 0)
    # and multiply by the class variable.
    # A version of the previous heuristic that eliminates underflow by using logs.
    candidate_scores = [(candidate, reduce(lambda x, y: x + y, [math.log(rs[candidate][f] + 1) for f in current_feature_set]) * rs[candidate][-1]) for candidate in candidate_feature_set]
    
    # Pick answer with the highest heuristic score.
    return sorted(candidate_scores, key = lambda x: x[1], reverse = True)[0][0]


# "Commenting out" the method (to leave syntax highlighting).
if False:
    # Compute the pairwise correlations. rs[i] is the correlations of the features with respect to feature i. rs[36] is
    # the correlation with respect to the class.
    rs = [pcc(norm_car_data_all, i) for i in xrange(37)]

    current_feature_set = []
    candidate_feature_set = range(36)

    current_distance_matrix = [[0] * len(norm_car_data) for i in xrange(len(norm_car_data))]
    for m in xrange(36):
        feature = best_feature(current_feature_set, candidate_feature_set, rs)
        current_feature_set.append(feature)
        candidate_feature_set.remove(feature)
        current_distance_matrix = sum_matrices(current_distance_matrix, feature_distances[feature])
        print '%s\nm = %2d: accuracy = %.6f\n\n' % (current_feature_set, m + 1, knn_loocv(car_data_classes, current_distance_matrix, (7,), (0, 1))[0][1])
