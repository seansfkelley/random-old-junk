data = ((0, 0), (1, 2), (1, 6), (2, 3), (3, 4), (5, 1), (4, 2), (5, 3), (6, 2), (7, 4))

def distance(d1, d2):
    return sum([(d1[i] - d2[i]) ** 2 for i in (0, 1)])

def distance_matrix(data):
    # Compute a 0-padded upper triangular matrix of distances.
    distance_upper_tri = [[0.0] * i + [distance(data[i], data[j]) for j in xrange(i, len(data))] for i in xrange(len(data))]
    # Convert upper triangular matrix into a full matrix (reflect across diagonal) to make accessing one element's distances easier.
    return [([distance_upper_tri[j][i] for j in xrange(i)] + distance_upper_tri[i][i:len(data)]) for i in xrange(len(data))]

m = distance_matrix(data)

for row in m:
    for element in row:
        print '%2d' % element,
    print
    
core_objects = [sum([1 if element <= 2 else 0 for element in row]) >= 3 for row in m]

print core_objects

for row in m:
    for element in row:
        print ('1' if element <= 2 else '0'),
    print
