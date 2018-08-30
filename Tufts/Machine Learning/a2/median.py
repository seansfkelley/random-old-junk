import sys

output = open('median-' + sys.argv[1], 'w')

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

median = [map(lambda x: float(x[i]), filter(lambda x: x[i] != '?', train_data)) for i in xrange(4)]
median = [sorted(median[i])[len(median[i]) / 2] for i in xrange(4)]

for t in train_data:
    t = map(str, [median[i] if t[i] == '?' else t[i] for i in xrange(4)] + t[4:])
    output.write(','.join(t) + '\n')