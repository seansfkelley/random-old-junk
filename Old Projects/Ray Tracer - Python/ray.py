from visual import vector, dot, cross, norm, rotate
from random import randint, seed
from operator import indexOf
from math import pi, sqrt
from EasyDialogs import *
import struct
import time
import os

#log=open('#log.txt', 'w')

#render options!
BKRD_COLOR=(1,1,1)
AMBIENCE=.3
CAMERA=vector(1500,1000,1000)
FOCUS_POINT=vector(0,0,0)
CANVAS=(64,64)
RESOLUTION=2.0#pixels per real world units, or scale/zoom. must be float
TOTAL_AREA=CANVAS[0]*CANVAS[1]
GRID_DIST=CAMERA.mag/1.3#temp value, set to whatever you like
CAM_ROTATION=0#radians, rotates the render clockwise (camera CCW)
T_THRESHOLD=.001#collisions for t less than this value are not counted (for ignoring rounding error, always POSITIVE)
MAX_DEPTH=5#number of objects to go through when calculating transparency
MAX_BOUNCES=10#maximum number of reflective bounces
FILL_COLOR=(1,0,1)#the color to fill unused space from a line in incomplete images
AUTOSAVE=True
DATA_FILE=True

#terrain options!
X_SIZE=15
Z_SIZE=15
MAX_RAD=8
HEIGHT=400
ITERATIONS=100
TER_BOX_SIZE=40
FLATTEN=2

class Ray:
    def __init__(self, org, direct, lite=None):
        self.origin=org
        self.direction=norm(direct)
        if lite==None:
            lite=[1.0,1.0,1.0]
        self.light=lite

class Light:
    def __init__(self, pos, col, intense):
        self.position=vector(pos)
        self.color=(float(col[0]), float(col[1]), float(col[2]))
        self.intensity=intense
    def calcLight(self, collision):
        #log.write('calc light\n')
        temp=self.position-collision #from collision to light
        distance=temp.mag
        ray=Ray(vector(collision), temp)
        stuff=None
        objects=[]
        for s in g_shapes:
            stuff=s.collide(ray)
            if not stuff or stuff[1]<T_THRESHOLD or stuff[1]>distance:
                continue
            if stuff[0].trans==0:
                return [0,0,0]
            objects+=[stuff[:2]]
        objects.sort(lambda x,y: x[1]-y[1], reverse=True)
        #reversed so objects closest to self are first
        light=list(self.color)
        for o in objects:
            o[0].filterLight(light,ray,distance)
        factor=self.intensity/(4*pi*distance**2)
        for i in range3:
            light[i]*=factor
            if light[i]>1:
                light[i]=1
                #if the intensity is too great, its capped to one
        return light

class Plane:
    def __init__(self, points, col, transparency=0, reflectiveness=0, isRect=False):
        #if it's a rectangle, p1 and p3 are assumed to be opposite corner and the list in CCW order,
        #also if the plane isnt aligned with any pairs of axes the behavior is undefined
        self.p1,self.p2,self.p3=points
        self.pts=list(points)
        self.color=(float(col[0]), float(col[1]), float(col[2]))
        self.trans=transparency
        self.refl=reflectiveness
        self.rect=isRect
        self.gradColor=self.gradBase=self.gradHeight=None
        #gradColor is top if height>0, bottom otherwise
    def __str__(self):
        return'plane<%s, %s, %s>' % (self.p1, self.p2, self.p3)
    def collide(self, ray):
        #http://local.wasp.uwa.edu.au/~pbourke/geometry/planeline/
        #p1=ray.origin
        #p2=ray.direction+ray.origin
        normal=findPlaneNormal(self.pts)
        denom=dot(normal, ray.direction) #n dot (p2-p1)
        if denom==0:
            return None
        t=dot(normal, self.p3-ray.origin)/denom #n dot (p3-p1)
        if self.rect:
            point=ray.direction*t+ray.origin
            for i in range3:
                point[i]=round(point[i],6)
            x,y,z=point
            p=self.pts
            if (p[0].x<=x<=p[2].x or p[0].x>=x>=p[2].x) and\
               (p[0].y<=y<=p[2].y or p[0].y>=y>=p[2].y) and\
               (p[0].z<=z<=p[2].z or p[0].z>=z>=p[2].z):
                return [self, t, None]
            else:
                return None
        else:
            return [self, t, None]
    def findColor(self, ray, t, otherInfo):
        col=None
        if self.gradColor:
            collision=ray.direction*t+ray.origin
            t1, t2=vector(self.gradBase[0]), vector(self.gradBase[1])
            d1=distPointLine(t1, t2, collision)
            t1.y+=self.gradHeight
            t2.y+=self.gradHeight
            d2=distPointLine(t1, t2, collision)
            if d1+d2-self.gradHeight>.001:
                if d1-d2>0:
                    col=self.gradColor
                else:
                    col=self.color
            else:
                mod=d1/self.gradHeight
                col=[]
                for i in range3:
                    col+=[mod*self.gradColor[i]+(1-mod)*self.color[i]]
        return calcColor(self, ray, t, findPlaneNormal(self.pts), col)
    def filterLight(self, light, ray, tMax):
        for i in range3:
            light[i]*=(self.trans*self.color[i])

class RectPrism:
    def __init__(self, pos, size, col, transparency=0, reflectiveness=0):
        x,y,z=size
        pos=vector(pos)
        self.length=x
        self.height=y
        self.depth=z
        self.position=pos
        self.color=(float(col[0]), float(col[1]), float(col[2]))
        self.trans=transparency
        self.refl=reflectiveness
        x/=2.0
        y/=2.0
        z/=2.0
        #see Plane.__init__ comment to understand the ordering here
        self.planes=[Plane([pos+vector(-x,y,z),pos+vector(-x,y,-z),pos+vector(-x,-y,-z)],
                           self.color,self.trans,self.refl,True),#-x
                     Plane([pos+vector(x,y,z),pos+vector(-x,y,z),pos+vector(-x,-y,z)],
                           self.color,self.trans,self.refl,True),#z
                     Plane([pos+vector(x,y,-z),pos+vector(x,y,z),pos+vector(x,-y,z)],
                           self.color,self.trans,self.refl,True),#x
                     Plane([pos+vector(-x,y,-z),pos+vector(x,y,-z),pos+vector(x,-y,-z)],
                           self.color,self.trans,self.refl,True),#-z
                     Plane([pos+vector(x,-y,-z),pos+vector(x,-y,z),pos+vector(-x,-y,z)],
                           self.color,self.trans,self.refl,True),#-y
                     Plane([pos+vector(x,y,z),pos+vector(x,y,-z),pos+vector(-x,y,-z)],
                           self.color,self.trans,self.refl,True)]#y
    def collide(self, ray, tMax=0):
        distance=-1
        values=None
        hits=0
        for p in self.planes:
            stuff=p.collide(ray)
            if stuff:
                t=stuff[1]
##                if indexOf(self.planes,p)==5:
##                    print 'trying topside of',self,'distance',t
                if tMax and t<tMax:
                    hits+=1
                    continue
                if t>T_THRESHOLD and (distance==-1 or t<distance):
                    values=[self,t,indexOf(self.planes,p)]
                    distance=t
        if tMax:
            return hits
##        if values and values[2]==5:
##            print 'hit topside on',self,'at',self.position,'t is',values[1]
        if values:
            pass
            #log.write('hit %s at %s\n' % (self,values[1]))
        return values
    def findColor(self, ray, t, otherInfo):
        return self.planes[otherInfo].findColor(ray, t, None)
    def filterLight(self, light, ray, tMax):
        hits=self.collide(ray, tMax)
        for i in range3:
            light[i]*=((self.trans*self.color[i])**hits)

class Sphere:
    def __init__(self, pos, rad, col, transparency=0, reflectiveness=0):
        self.position=vector(pos)
        self.radius=rad
        self.color=(float(col[0]), float(col[1]), float(col[2]))
        self.trans=transparency
        self.refl=reflectiveness
    def collide(self, ray, tMax=0):
        #lightTest is assuming collision is already confirmed
        #http://www.siggraph.org/education/materials/HyperGraph/raytrace/rtinter1.htm
        #since ray is normalized, a is 1 and can be ignored
        rx,ry,rz=ray.direction
        x0,y0,z0=ray.origin
        sx,sy,sz=self.position
        b=2*(rx*(x0-sx)+ry*(y0-sy)+rz*(z0-sz))
        c=(x0-sx)**2+(y0-sy)**2+(z0-sz)**2-self.radius**2
        d=b**2-4*c#discriminant
        if d<0:
            return None
        elif d==0:
            if tMax:
                return 1
            t=-b/2
        else:
            if tMax:
                hits=0
                if (-b-sqrt(d))/2<tMax:
                    hits+=1
                if (-b+sqrt(d))/2<tMax:
                    hits+=1
                return hits
            t=(-b-sqrt(d))/2
            if t<T_THRESHOLD:#meaning its backwards
                t=(-b+sqrt(d))/2
                if t<T_THRESHOLD:#still backwards! its completely behind the ray
                    return None
        #log.write('hit %s at %d\n' % (self,t))
        return [self,t,None]
    def findColor(self, ray, t, otherInfo):
        return calcColor(self, ray, t, norm(ray.direction*t+ray.origin-self.position))
    def filterLight(self, light, ray, tMax):
        hits=self.collide(ray, tMax)
        for i in range3:
            light[i]*=((self.trans*self.color[i])**hits)

def calcColor(shape, ray, t, normal, defColor=None):
    #log.write('calcColor\n')
    if defColor==None:
        defColor=shape.color
    tColor=transparent(shape.trans, ray, t, defColor)
    rColor=reflect(shape.refl, ray, t, defColor, normal)
    color=[]
    for i in range3:
        color+=[defColor[i]*(1-shape.refl-shape.trans)+shape.trans*tColor[i]+shape.refl*rColor[i]]
    return lighting(color,ray.direction*t+ray.origin, normal)

def transparent(trans, ray, t, color):
    #log.write('transparent\n')
    global g_depth
    color=list(color)
    if trans==0 or g_depth==MAX_DEPTH:
        for i in range3:
            color[i]*=ray.light[i]
        return color
    g_depth+=1
    newRay=Ray(ray.direction*t+ray.origin, ray.direction, list(color))
    addColor=rayTrace(newRay)
    for i in range3:
        color[i]*=((1-trans)*ray.light[i])
        color[i]+=(addColor[i]*trans)
    return color

def reflect(refl, ray, t, color, normal):
    #log.write('reflect\n')
    global g_bounces
    color=list(color)
    if refl==0 or g_bounces==MAX_BOUNCES:
        for i in range3:
            color[i]*=ray.light[i]
        return color
    g_bounces+=1
    newDir=-rotate(ray.direction, angle=pi, axis=normal)
    #newDir=ray.direction+normal*2*(-dot(normal,ray.direction))
    newRay=Ray(ray.direction*t+ray.origin, newDir, list(color))
    reflected=rayTrace(newRay)
    for i in range3:
        color[i]*=((1-refl)*ray.light[i])
        color[i]+=(reflected[i]*refl)
    return color

def lighting(color, collision, normal):
    #log.write('lighting\n')
    #global g_lights

    #sum then truncate
    total=[0,0,0]
    for light in g_lights:
        direction=norm(light.position-collision)
        shade=dot(direction, normal)
        if shade<0:
            shade=0
        light=light.calcLight(collision)
        for i in range3:
            total[i]+=light[i]*shade
    result=[]
    for i in range3:
        if total[i]>1:
            total[i]=1
        result+=[color[i]*(AMBIENCE+(1-AMBIENCE)*total[i])]
    return result

##    light=g_lights
##    direction=norm(light.position-collision)
##    shade=dot(direction, normal)
##    if shade<0:
##        shade=0
##    light=light.calcLight(collision)
##    result=[]
##    for i in range3:
##        result+=[color[i]*(AMBIENCE+(1-AMBIENCE)*shade*light[i])]
##    return result

def angleCCW(compAxis, rotAxis, vec, ang):
    ang+=2*pi
    if ang==0 or ang==2*pi:
        return 0
    if not equalVector(norm(rotate(vector(vec), angle=ang, axis=rotAxis)), norm(compAxis)):
        return 2*pi-ang
    return ang

def equalVector(v1, v2):
    for i in range3:
        if abs(v1[i]-v2[i])>.001:
            return False
    return True

def distPointLine(l1, l2, p):
    AB=l2-l1
    AP=p-l1
    return cross(AB, AP).mag/AB.mag

def findPlaneNormal(plane):
    #n = (b - a) x (c - a)
    p1,p2,p3=plane
    return norm(cross((p2-p1),(p3-p1)))

def rayTrace(ray):
    #log.write('tracing ray with org %s and dir %s\n' % (ray.origin, ray.direction))
    distance=-1
    target=None
    for s in g_shapes:
        #collide should return [self,t,other_information]
        collision=s.collide(ray)
        if collision and collision[1]>0 and (collision[1]<distance or distance==-1):
            target,distance, otherInfo=collision
    if target:
        return target.findColor(ray, distance, otherInfo)
    else:
        return BKRD_COLOR

def render():
    global g_firstPixel, g_rowEnd, g_colEnd, g_lastPixel, g_depth, g_bounces
    t=time.time()
    progress=ProgressBar('Rendering...',TOTAL_AREA, '0 of %d pixels' % TOTAL_AREA)
    y=0
    bytes=[None]*CANVAS[1]
    yDirect=norm(g_colEnd-g_firstPixel)/RESOLUTION
    yDirectOpp=norm(g_lastPixel-g_rowEnd)/RESOLUTION
    #print 'yDirect',yDirect,'yDirectOpp',yDirectOpp
    while y<CANVAS[1]:
        bytes[y]=''
        x=0
        pixel=vector(g_firstPixel)
        #print g_firstPixel,'g_firstPixel',g_rowEnd,'g_rowEnd'
        xDirect=norm(g_rowEnd-g_firstPixel)/RESOLUTION
        #print 'xDirect',xDirect
        while x<CANVAS[0]:
            #log.write('finding pixel (%d,%d)\n' % (x,y))
            g_depth=g_bounces=0
            color=list(rayTrace(Ray(vector(pixel), pixel-CAMERA)))
            for i in range3:
                color[i]=int(color[i]*255)
            r,g,b=color
            bytes[y]+=struct.pack('3B',b,g,r)
            x+=1
            pixel+=xDirect
            try:
                progress.inc()
                progress.label('%d of %d pixels' % (progress.curval, TOTAL_AREA))
            except KeyboardInterrupt:
                choice=AskYesNoCancel('Would you like to save the incomplete image?', 0, 'No', 'Cancel', 'Yes')
                if choice==-1:#yes
                    writeFile(bytes, t, y+1, 'User stopped after %d pixels, %.2f%% completed.'\
                              % (progress.curval, 100*float(progress.curval)/TOTAL_AREA))#y is one less than the equivalent line number
                    exit()
                elif choice==0:#cancel
                    del progress
                    progress=ProgressBar('Rendering...',TOTAL_AREA, '%d of %d pixels'\
                                         % (y*CANVAS[1]+x, TOTAL_AREA))
                    progress.set(y*CANVAS[1]+x)
                else:#no
                    exit()
        bytes[y]+=(struct.pack('B',0)*((4-(x*3)%4)%4))
        y+=1
        g_firstPixel+=yDirect
        g_rowEnd+=yDirectOpp
    del progress
    return [bytes, t]

def writeFile(bytes, startTime, incomplete=False, notes='None'):
    t=int(time.time()-startTime)
    hours=t/3600
    t%=3600
    minutes=t/60
    t%=60
    temp=time.strftime('%c', time.localtime())
    defName=''
    for l in temp:
        if l in ':/':
            defName+='.'
        else:
            defName+=l
    defName=defName.split(' ')
    defName='render-d'+defName[0]+'-t'+defName[1]
    if incomplete:
        defName+='-inc'
    defName+='.bmp'
    if DATA_FILE:
        f=open(defName[:-4]+'.txt', 'w')
        f.writelines(['dimensions: %dx%d, %d pixels total\n' % (CANVAS[0], CANVAS[1], TOTAL_AREA),
                      'time: %d:%02d:%02d\n' % (hours, minutes, t),
                      'shape count: %d\n' % len(g_shapes),
                      'camera: %s\n' % CAMERA,
                      'focus: %s\n' % FOCUS_POINT,
                      'grid distance: %.3f\n' % GRID_DIST,
                      'resolution: %.3f\n' % RESOLUTION,
                      'rotation: %.3f\n' % CAM_ROTATION,
                      '\nnotes: %s\n' % notes])
        f.close()
    if AUTOSAVE:
        f=open(defName, 'wb')
    else:
        while True:
            name=AskFileForSave(savedFileName=defName, fileType='bmp')
            if name==None:
                if AskYesNoCancel('Are you sure?', 1, 'No', '', 'Yes')==-1:#yes
                    exit()
                continue
            #dialog already asks about overwrite
            if os.path.exists(name):
                os.unlink(name)
            f=open(name, 'wb')
            break
    
    #http://www.fortunecity.com/skyscraper/windows/364/bmpffrmt.html
    #total header size: 54 bytes
    #short 19778 = 2 chars: BM
    if not incomplete:
        temp=struct.pack('HIHHI',19778,3*TOTAL_AREA+54,0,0,54)
        bmpFileHeader=temp[:2]+temp[4:] #adds 2 extra bytes for 19778 for some reason
        bmpInfoHeader=struct.pack('3I2H6I',40,CANVAS[0],CANVAS[1],1,24,0,0,0,0,0,0)
    else:
        temp=struct.pack('HIHHI',19778,3*CANVAS[0]*incomplete+54,0,0,54)
        bmpFileHeader=temp[:2]+temp[4:]
        bmpInfoHeader=struct.pack('3I2H6I',40,CANVAS[0],incomplete,1,24,0,0,0,0,0,0)
        incomplete-=1#now using incomplete as an index, not a line number
        temp=len(bytes[incomplete])/3.0#3 bytes per pixel, need num pixels not bytes
        r,g,b=FILL_COLOR
        r,g,b=int(r*255),int(g*255),int(b*255)
        while temp<CANVAS[0]:
            bytes[incomplete]+=(struct.pack('3B',b,g,r))
            temp+=1
        bytes[incomplete]+=(struct.pack('B',0)*((4-(CANVAS[0]*3)%4)%4))
        while None in bytes:
            bytes.remove(None)
    f.write(bmpFileHeader+bmpInfoHeader)
    for i in range(-len(bytes)+1,1):
        f.write(bytes[-i])
    f.close()

def generateHills():
    #http://www.robot-frog.com/3d/hills/hill.html
    randPctSet=lambda: (randint(0,100)/100.0,randint(0,100)/100.0,randint(0,100)/100.0)
    progress=ProgressBar('Generating Terrain...', ITERATIONS, '0 of %d iterations' % ITERATIONS)
    terrain=[]
    for x in range(X_SIZE):
        terrain+=[[0]*Z_SIZE]
    maximum=0
    minimum=10**9
    for i in range(ITERATIONS):
        #center
        x1=randint(0,X_SIZE-1)
        z1=randint(0,Z_SIZE-1)
        #radius
        r=MAX_RAD*(randint(0,100)/100.0)
        for x2 in range(X_SIZE):
            for z2 in range(Z_SIZE):
                y=r**2-((x2-x1)**2+(z2-z1)**2)
                if y>0:
                    terrain[x2][z2]+=y
        try:
            progress.inc()
            progress.label('%d of %d iterations' % (i, ITERATIONS))
        except KeyboardInterrupt:
            if AskYesNoCancel('Are you sure?', 1, 'No', '', 'Yes')==-1:#yes
                exit()
            else:
                del progress
                progress=ProgressBar('Generating Terrain...',ITERATIONS, '%d of %d iterations'\
                                     % (i, ITERATIONS))
                progress.set(i)
    for x in range(X_SIZE):
        for z in range(Z_SIZE):
            value=terrain[x][z]
            if value>maximum:
                maximum=value
            elif value<minimum:
                minimum=value

##    #this is for writing to a .bmp to see the layout
##    x=X_SIZE
##    y=Z_SIZE
##
##    temp=struct.pack('HIHHI',19778,3*x*y+54,0,0,54)
##    FH=temp[:2]+temp[4:] #adds 2 extra bytes for 19778 for some reason
##    IH=struct.pack('3I2H6I',40,x,y,1,24,0,0,0,0,0,0)
##
##    f=open('terrain.bmp', 'wb')
##    f.write(FH+IH)
##
##    y1=0
##    while y1<y:
##        x1=0
##        while x1<x:
##            terrain[x1][y1]=(terrain[x1][y1]-minimum)/(maximum-minimum)
##            v=int(round(terrain[x1][y1]*255, 0))
##            if v>255:
##                v=255
##            f.write(struct.pack('3B', v,v,v))
##            x1+=1
##        f.write(struct.pack('B',0)*((4-(x*3)%4)%4))
##        y1+=1
##
##    f.close()
##
##    exit()

    for x in range(X_SIZE):
        for z in range(Z_SIZE):
            y=round((((terrain[x][z]-minimum)/(maximum-minimum))**FLATTEN)*HEIGHT, 3)
            g_shapes.append(RectPrism((x*TER_BOX_SIZE,y/2,z*TER_BOX_SIZE),
                                      (TER_BOX_SIZE,y,TER_BOX_SIZE),
                                      randPctSet()))
##    global g_shapes
##    for i in range(len(g_shapes)):
##        if g_shapes[i].height==0:
##            g_shapes[i]=g_shapes[i].planes[5]
##            break

def initializeGrid():
    global g_firstPixel,g_rowEnd,g_colEnd,g_lastPixel
    cameraOff=CAMERA-FOCUS_POINT

    xAxis, yAxis=vector(1,0,0), vector(0,1,0)

    XZcamera=vector(cameraOff)
    XZcamera.y=0

    XZangle=angleCCW(xAxis, yAxis, XZcamera, XZcamera.diff_angle(xAxis))

    secondAxis=rotate(XZcamera, angle=pi/2, axis=yAxis)

    tiltAngle=angleCCW(XZcamera, secondAxis, cameraOff, cameraOff.diff_angle(XZcamera))

    g_firstPixel=vector(0, CANVAS[1]/(2*RESOLUTION), CANVAS[0]/(2*RESOLUTION))
    g_colEnd=g_firstPixel-vector(0,CANVAS[1]/RESOLUTION,0)
    g_rowEnd=g_firstPixel-vector(0,0,CANVAS[0]/RESOLUTION)
    g_lastPixel=g_rowEnd-vector(0,CANVAS[1]/RESOLUTION,0)

    transform=lambda v: rotate(rotate(v, angle=-XZangle, axis=yAxis),
                               angle=tiltAngle, axis=secondAxis)+norm(cameraOff)*GRID_DIST

    g_firstPixelTemp=transform(g_firstPixel)
    g_colEndTemp=transform(g_colEnd)
    g_rowEndTemp=transform(g_rowEnd)
    g_lastPixelTemp=transform(g_lastPixel)

    if g_firstPixelTemp.mag!=g_colEndTemp.mag:
        #these points will always move in opposite directions, thus the mags will not be equal
        #if rotated the wrong way
        transform=lambda v: rotate(rotate(v, angle=-XZangle, axis=yAxis),
                                   angle=-tiltAngle, axis=secondAxis)+norm(cameraOff)*GRID_DIST
        g_firstPixelTemp=transform(g_firstPixel)
        g_colEndTemp=transform(g_colEnd)
        g_rowEndTemp=transform(g_rowEnd)
        g_lastPixelTemp=transform(g_lastPixel)
        
    transform=lambda v: rotate(v, angle=CAM_ROTATION, axis=cameraOff)+FOCUS_POINT
    g_firstPixel=transform(g_firstPixelTemp)
    g_colEnd=transform(g_colEndTemp)
    g_rowEnd=transform(g_rowEndTemp)
    g_lastPixel=transform(g_lastPixelTemp)

if __name__=='__main__':
    g_firstPixel=g_rowEnd=g_colEnd=g_lastPixel=None
    g_shapes=[]
    g_depth=g_bounces=0
    #g_lights=[Light((0,250,-1000), (1,1,1), 5*10**7), Light((0,250,1000), (1,1,1), 10**8)]
    g_lights=[Light((1000,750,500), (1,1,1), 10**7)]
    range3=(0,1,2)#so range(3) doesnt have to be called a million times over

    #i use randint here because i want to include the endpoint
    #seed(277)
    randPctSet=lambda: (randint(0,100)/100.0,randint(0,100)/100.0,randint(0,100)/100.0)
    randIntSet=lambda i,j: (randint(i,j),randint(i,j),randint(i,j))

    #color=randPctSet()
    
    z=-40
    a=False
    while z<=80:
        x=-80
        if a:
            x+=40
        a=not a
        while x<=80:
            g_shapes.append(RectPrism((x,0,z),(40,40,40),randPctSet()))
            x+=80
        z+=40

    z=-40
    a=True
    while z<=80:
        x=-80
        if a:
            x+=40
        a=not a
        while x<=80:
            g_shapes.append(RectPrism((x,-40,z),(40,40,40),randPctSet()))
            x+=80
        z+=40

##    g_shapes.append(RectPrism((0,0,0),(96,96,96),(.5,.5,.5)))
##    g_shapes.append(RectPrism((96,0,0), (96,96,96), (.5,.5,.5)))
##    g_shapes.append(RectPrism((-96,0,0), (96,96,96), (.5,.5,.5)))
##    g_shapes.append(Plane((vector(0,0,-128), vector(0,128,-128), vector(128,0,-128)),(1,1,1),0,1))
##    g_shapes.append(Sphere((-64,64,-32), 48, (.8,.8,.8), 0, .9))
##    g_shapes.append(Sphere((64,192,64), 48, (.8,.8,.8), 0, .9))
##    g_shapes.append(Sphere((0,0,0), 24, (.5,.5,.5)))
##    g_shapes.append(RectPrism((0,0,0), (3000,3000,3000), (.7,.7,.7)))
    
##    g_shapes.append(RectPrism((0,0,750), (1000,1000,3000), (0,.66,1)))
##    r=g_shapes[-1]
##    for i in range(4):
##        r.planes[i].gradColor=(0,0,0)
##        r.planes[i].gradHeight=1000
##    #-x,z,x,-z
##    r.planes[0].gradBase=[vector(-500,-500,500), vector(-500,-500,-500)]
##    r.planes[1].gradBase=[vector(-500,-500,2250), vector(500,-500,2250)]
##    r.planes[2].gradBase=[vector(500,-500,500), vector(500,-500,-500)]
##    r.planes[3].gradBase=[vector(500,-500,-750), vector(-500,-500,-750)]
##    #-y,y
##    r.planes[5].color=(0,0,0)

##    for i in range(20):
##        g_shapes.append(RectPrism(randIntSet(-100,100), (32,32,32), randPctSet(), randint(25,75)/100.0, 0))

##    arrow(shaftwidth=25,axis=vector(1000,0,0),color=color.red)
##    arrow(shaftwidth=25,axis=vector(0,1000,0),color=color.green)
##    arrow(shaftwidth=25,axis=vector(0,0,1000),color=color.blue)

##    generateHills()

##    g_shapes.append(RectPrism((0,0,0), (1,0,1), randPctSet()))

##    for i in (-1,0,1):
##        for j in (-1,0,1):
##            g_shapes.append(RectPrism((i*40, 0, j*40), (40,40,40), randPctSet()))
    
    initializeGrid()
    bytes,start=render()
    writeFile(bytes, start)

    #log.close()

#http://www.siggraph.org/education/materials/HyperGraph/raytrace/rtinter1.htm

#to do
    #networking/multiprocessing
    #plane.isRect=True and gradients should work in any direction
    #scatter (optional render setting)
    #averaging of multiple vectors for one pixel
    #sky - use steepness of escape vector to calculate
    #save/load with pickle and pack/unpack (to and from list) for objects
