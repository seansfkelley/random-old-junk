import fileinput
import sys

DUPLICATE_DEPTS = False

NODE = '    {nodeName:"%s", is_person:%s},'
LINK = '    {source:%d, target:%d, person_person_link:%s},'

person_person_links = {}
person_dept_links = {}

for l in fileinput.input():
    l = l.rstrip()
    who, collaborators, departments = l.split(',')
    person_person_links[who] = collaborators.split(';')
    person_dept_links[who] = departments.split(';')

print 'var data = {'
print '  nodes:['

i = 0
node_indices = {}
for (source, targets) in person_person_links.items():
    for p in [source] + targets:
        if p and p not in node_indices:
            print NODE % (p, 1)
            node_indices[p] = i
            i += 1

if DUPLICATE_DEPTS:
    dept_indices = {}
    
    for (source, targets) in person_dept_links.items():
        if source and source not in node_indices:
            print NODE % (p, 1)
            node_indices[p] = i
            i += 1
    
        for p in targets:
            if p:
                if p not in dept_indices:
                    print NODE % (p, 0)
                    dept_indices[p] = [i]
                    i += 1
                else:
                    print NODE % (p, 0)
                    dept_indices[p].append(i)
                    i += 1

    print '  ],'
    print '  links:['

    edges = []
    
    for (source, targets) in person_person_links.items():
        for t in targets:
            if t and (node_indices[source], node_indices[t]) not in edges:
                print LINK % (node_indices[source], node_indices[t], 'true')
                edges.append((node_indices[source], node_indices[t]))
                edges.append((node_indices[t], node_indices[source]))

    for (source, targets) in person_dept_links.items():
        for t in targets:
            if t and (node_indices[source], dept_indices[t][-1]) not in edges:
                print LINK % (node_indices[source], dept_indices[t][-1], 'false')
                edges.append((node_indices[source], dept_indices[t][-1]))
                edges.append((dept_indices[t][-1], node_indices[source]))
                dept_indices[t].pop()
    
else:
    for (source, targets) in person_dept_links.items():
        if source and source not in node_indices:
            print NODE % (p, 1)
            node_indices[p] = i
            i += 1
    
        for p in targets:
            if p and p not in node_indices:
                print NODE % (p, 0)
                node_indices[p] = i
                i += 1

    print '  ],'
    print '  links:['

    edges = []

    for (source, targets) in person_person_links.items():
        for t in targets:
            if t and (source, t) not in edges:
                print LINK % (node_indices[source], node_indices[t], 'true')
                edges.append((source, t))
                edges.append((t, source))

    for (source, targets) in person_dept_links.items():
        for t in targets:
            if t and (source, t) not in edges:
                print LINK % (node_indices[source], node_indices[t], 'false')
                edges.append((source, t))
                edges.append((t, source))

print '  ]'
print '};'