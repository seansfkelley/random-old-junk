import fileinput
found_first = False

for line in fileinput.input():
    line = line.strip()
    line2 = line.split(' ')
    if len(line2) > 1 and line2[1] == 'Beginning':
        found_first = True
        continue
    if not found_first:
        try:
            int(line2[0])
            print '# ' +  ' '.join(line2[1:])
        except ValueError:
            if len(line) > 0:
                print '# ' + line
    elif len(line) > 0:
        print line2[1] + ',' + line2[2]
