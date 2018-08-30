import fileinput
import re

class Struct:
    pass

nodes = {}
edges = []

for line in fileinput.input():
    line = line[:-1]
    line = line.split(' ')
    if len(line) >= 2 and re.match('\[shape=', line[1]):
        n = Struct()
        n.name = line[0].strip('\"')
        n.label = ' '.join(line[2:]).split('\"')[1]
        nodes[n.name] = n
    elif len(line) >= 2 and line[1] == '->':
        e = Struct()
        e.source = line[0].strip('\"')
        e.target = line[2].strip('\"')
        edges.append(e)

print r'<graphml xmlns="http://graphml.graphdrawing.org/xmlns">'
print r'<graph edgedefault="undirected">'
print
print r'<!-- data schema -->'
print r'<key id="name" for="node" attr.name="name" attr.type="string"/>'
print
print r'<!-- nodes -->'

for n in nodes.values():
    print r'<node id="' + n.name + r'">'
    print r'    <data key="name">' + n.label + r'</data>'
    print r'</node>'

print r'<!-- connections -->'
print r'<!-- edges -->'

for e in edges:
    print r'<edge source="' + e.source + r'" target="' + e.target + r'"></edge>'

print r'</graph>'
print r'</graphml>'