import re
import fileinput

class Timestep:
    pass

timesteps = []

for line in fileinput.input():
    line = line.split(' ')
    if len(line) == 1:
        continue
    if line[0] == 'Processes:':
        timesteps.append(Timestep())
        current_timestep = timesteps[-1]
        current_timestep.processes = int(line[1])
        # current_timestep.running = int(line[3])
        # current_timestep.sleeping = int(line[5])
        # current_timestep.threads = int(line[7])
    elif line[0] == 'Load':
        current_timestep.load_avg = float(line[2][:-1]) * 100
    elif line[0] == 'CPU':
        current_timestep.total_usage = 100 - float(line[6][:-1])
    elif line[0] == 'PhysMem:':
        current_timestep.memory = int(line[7][:-1])

print 'Seconds\tCPU Usage\tLoad Average\tMemory Usage'

i = 1
for t in timesteps:
    print '%d\t%f\t%f\t%d' % (i, t.total_usage, t.load_avg, t.memory)
    i += 1
