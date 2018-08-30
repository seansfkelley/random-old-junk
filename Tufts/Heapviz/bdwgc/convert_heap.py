import sys
import os

if len(sys.argv) < 2:
	print 'Usage: %s heap_dump_filename' % sys.argv[0]

with open(sys.argv[1], 'r') as f:
    while f.readline() != 'dumping heap\n': pass

    # Source -> target mappings as integers.
    graph = {}
    sizes = {}
    while True:
        l = f.readline().strip()
        if l == 'finish pushing roots': break
        # Add an edge from Fake root to this actual root.
        graph.setdefault(0, []).append(int(l.split('>')[1], 16))
        # Skip the pointer layout for the memory blocks.
        f.readline()
    
    while True:
        l = f.readline().strip()
        if len(l) == 0 or l == 'end heap dump': break
        if '(nil)' in l:
            f.readline() # Skip the pointer layout.
            continue

        s, t = l.split('>')
        s = s[:s.find('[')] # Drop offset for now.
        s, t = int(s, 16), int(t, 16)
        # Add edge.
        graph.setdefault(s, []).append(t)
        # Add record for target. Even if it ultimately has no outgoing edges, this simplifies the conversion to GraphML.
        graph.setdefault(t, [])
        # Log the size of target. 
        # Ignored for now.
        # sizes[t] = sz
        # Skip the pointer layout for the memory blocks.
        f.readline()

with open(os.path.splitext(sys.argv[1])[0] + '.xml', 'w') as f:
    # Boilerplate header.
    f.write('''<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">

<key id="type" for="node" attr.name="type" attr.type="string">
  <default>C/C++ memory block</default>
</key>
<key id="members" for="node" attr.name="members" attr.type="string">
  <default></default>
</key>
<key id="count" for="node" attr.name="count" attr.type="int">
  <default>1</default>
</key>
<key id="size" for="node" attr.name="size" attr.type="int">
  <default>0</default>
</key>

<graph edgedefault="directed">

<node id="0x0">
  <data key="type">Fake root</data>
</node>
''')

    for n in graph.iterkeys():
        if n != 0:
            f.write('<node id="0x%x">\n  <data key="size">%d</data>\n  <data key="type">0x%x</data>\n</node>\n' % (n, sizes.get(n, 0), n))
    
    for (s, ts) in graph.iteritems():
        for t in ts:
            f.write('<edge source="0x%x" target="0x%x"/>\n' % (s, t))
    
    f.write('</graph>\n</graphml>\n')
