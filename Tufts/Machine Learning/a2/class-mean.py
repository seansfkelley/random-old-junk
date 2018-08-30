import sys

output = open('class-mean-' + sys.argv[1], 'w')

f = open(sys.argv[1], 'r')

for line in f:
    output.write(line)
    if line.lower() == '@data\n':
        break

train_data = []
for line in f:
    d = line.strip().split(',')
    if len(d) >= 4:
        train_data.append(d)

f.close()

mean = [map(lambda x: (float(x[i]), x[4]), filter(lambda x: x[i] != '?', train_data)) for i in xrange(4)]
mean = [[filter(lambda x: x[1] == name, mean[i]) for i in xrange(4)] for name in ('versicolor', 'virginica', 'setosa')]
mean = [[map(lambda x: x[0], mean[j][i]) for i in xrange(4)] for j in xrange(3)]
mean = [map(lambda x: sum(x) / len(x), mean[i]) for i in xrange(3)]

classmap = { 'versicolor' : 0, 'virginica' : 1, 'setosa' : 2 }

for t in train_data:
    t = map(str, [mean[classmap[t[4]]][i] if t[i] == '?' else t[i] for i in xrange(4)] + t[4:])
    output.write(','.join(t) + '\n')

output.close()