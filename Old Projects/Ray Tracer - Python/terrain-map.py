import struct
from random import randint
import sys

x=1366
y=768

iters=2000

maxrad=50

flatten=2

temp=struct.pack('HIHHI',19778,3*x*y+54,0,0,54)
FH=temp[:2]+temp[4:] #adds 2 extra bytes for 19778 for some reason
IH=struct.pack('3I2H6I',40,x,y,1,24,0,0,0,0,0,0)

terrain=[]

for a in range(x):
    terrain+=[[0]*y]

#http://www.robot-frog.com/3d/hills/hill.html

maximum=0
minimum=1000000

for i in range(iters):
    print i,
    sys.stdout.flush()
    x1=randint(0,x-1)
    y1=randint(0,y-1)
    r=maxrad*(randint(0,100)/100.0)
    for x2 in range(x):
        for y2 in range(y):
            z=r**2-((x2-x1)**2+(y2-y1)**2)
            if z>0:
                terrain[x2][y2]+=z
                if terrain[x2][y2]>maximum:
                    maximum=terrain[x2][y2]
                elif terrain[x2][y2]<minimum:
                    minimum=terrain[x2][y2]

f=open('terrain.bmp', 'wb')
f.write(FH+IH)

y1=0
while y1<y:
    x1=0
    while x1<x:
        terrain[x1][y1]=((terrain[x1][y1]-minimum)/(maximum-minimum))**flatten
        v=int(round(terrain[x1][y1]*255, 0))
        if v>255:
            v=255
        f.write(struct.pack('3B', v,v,v))
        x1+=1
    f.write(struct.pack('B',0)*((4-(x*3)%4)%4))
    y1+=1

f.close()
