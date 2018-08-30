#INDEX-----------------------------------------------------------
 #CONSTANTS/IMPORTS
 #VARIABLES
 #CLASSES
 #FUNCTIONS
  #Mathematical
  #Sort/Search-Related
  #Drawing
  #Deformation
  #Miscellaneous
 #EXECUTION

#CONSTANTS/IMPORTS-----------------------------------------------
from visual import *
from random import randint
DEFAULT_NODE_COLOR=(.5,.5,.5)
SELECT_NODE_COLOR=(.7,.7,.7)
PAPER_FRONT_COLOR=(1,1,1)
PAPER_BACK_COLOR=(.5,.5,.5)
SNAP_THRESHOLD=math.pi/12
AUTOSCALING=0
DEFAULT_SQUARE=[vector(-512,-512,0), vector(512,-512,0), vector(512,512,0), vector(-512,512,0)]
#DEFAULT_SQUARE=[vector(0,0,0), vector(-512,-512,0), vector(512,-512,0), vector(512,512,0), vector(-512,512,0)]

#VARIABLES-------------------------------------------------------
scene.ambient=.9
m=scene.mouse
kb=scene.kb
select=False
pointSelect=[]

#CLASSES---------------------------------------------------------
class PaperInfo:
    def __init__(self, verts, defFrame):
        self.vertices=verts
        self.frame=defFrame

class Triangle:
    def __init__(self, v1, v2, v3):
        self.vertices=[v1, v2, v3]
    def createBackside(self):
        return Triangle(self.vertices[2], self.vertices[1], self.vertices[0])
   
class pLine:
    def __init__(self,x,xt,y,yt,z,zt):
        self.values=[x,xt,y,yt,z,zt]
    def __init__(self,p1,p2):
        self.values=[]
        for i in range(0,3):
            self.values+=[p1[i]]+[p2[i]-p1[i]]
    def solvePoint(self, t):
        tempPoint=[]
        for i in range(0,3):
            tempPoint+=[self.values[i*2]+self.values[i*2+1]*t]
        return tempPoint

#FUNCTIONS-------------------------------------------------------

#----------------------------------------------------Mathematical
def snapAngle(center, dragPoint, snapTo):
    #opp=distP2L(center, snapTo, dragPoint)
    #hyp=mag(vector(snapTo)-vector(center))
    #r=math.asin(opp/hyp)
    #sphere(pos=center, radius=20)
    #law of cosines
    a=distP2P(center, dragPoint)
    b=distP2P(center, snapTo)
    c=distP2P(snapTo, dragPoint)
    r=math.acos((c**2-a**2-b**2)/(-2*a*b))
    print r
    return r

def distP2P(p1, p2):
    """Returns float."""
    return abs(mag(vector(p2)-vector(p1)))

def distP2L(l1, l2, p):
    """Returns float."""
    A=vector(l1)
    B=vector(l2)
    P=vector(p)
    AB=B-A
    AP=P-A
    return mag(cross(AP, AB))/mag(AB)

def polarAngle(x,y):
    rad=math.atan(float(y)/float(x))
    if x<0:
        rad+=math.pi
    elif y<0:
        rad+=math.pi*2
    return rad

#---------------------------------------------Sort/Search-related
def equalVector(v1, v2):
    for i in range(0,3):
        if v1[i]!=v2[i]:
            return False
    return True

def triToVertList(triangleList):
    vList=[]
    for tri in triangleList:
        vList+=tri.vertices
    return vList

def sortVertices(vList):
    """Sorts vertices in order according to their polar angle from (0,0) in a
    clockwise direction from the positive x-axis."""
    vl=[vList[0]]
    if(polarAngle(vl[0].x,vl[0].y)<=polarAngle(vList[1].x,vList[1].y)):
        vl+=[vList[1]]
    else:
        vl=[vList[1]]+vl
    for i in vList:
        if i==vList[0] or i==vList[1]:
            continue
        if(polarAngle(vl[0].x,vl[0].y)>=polarAngle(i.x,i.y)):
            vl=[i]+vl
            continue
        elif(polarAngle(vl[-1].x,vl[-1].y)<=polarAngle(i.x,i.y)):
            vl+=[i]
            continue
        j=1
        while j<len(vl):
            if polarAngle(vl[j-1].x,vl[j-1].y)<=polarAngle(i.x,i.y)<=polarAngle(vl[j].x,vl[j].y):
                vl=vl[:j]+[i]+vl[j:]
                break
            j+=1
    return vl

def triAtPoint(point, triList):
    atPoint=[]
    for i in triList:
        for j in range(0,3):
            if equalVector(i.vertices[j], point):
                atPoint+=[i]
    return atPoint

#---------------------------------------------------------Drawing
def drawPolygonSimple(withCenter=False):
    #doesnt work for some shapes with any 3 vertices forming a triangle
    #that isnt supposed to be filled in
    vList=PAPER.vertices
    i=2
    triList=[]
    while i<len(vList):
        tempTri=Triangle(vList[0], vList[i-1], vList[i])
        triList=triList[:len(triList)/2]+[tempTri]+triList[len(triList)/2:]
        triList+=[tempTri.createBackside()]
        i+=1
    if withCenter:
        tempTri=Triangle(vList[0], vList[-1], vList[1])
        triList=triList[:len(triList)/2]+[tempTri]+triList[len(triList)/2:]
        triList+=[tempTri.createBackside()]
    vectorList=triToVertList(triList)
    newFrame=frame()
    faces(frame=newFrame, pos=vectorList[:len(vectorList)/2], color=PAPER_FRONT_COLOR)
    faces(frame=newFrame, pos=vectorList[len(vectorList)/2:], color=PAPER_BACK_COLOR)
    if PAPER.frame:
        for o in PAPER.frame.objects:
            o.visible=0
    PAPER.frame=newFrame

def drawPolygonCenterSimple(center):
    #doesnt work for some shapes with any 3 vertices forming a triangle
    #that isnt supposed to be filled in
    vList=PAPER.vertices
    center=vector(center)
    i=1
    triList=[]
    while i<len(vList):
        tempTri=Triangle(center, vList[i-1], vList[i])
        triList=triList[:len(triList)/2]+[tempTri]+triList[len(triList)/2:]
        triList+=[tempTri.createBackside()]
        i+=1
    tempTri=Triangle(center, vList[-1], vList[0])
    triList=triList[:len(triList)/2]+[tempTri]+triList[len(triList)/2:]
    triList+=[tempTri.createBackside()]
    vectorList=triToVertList(triList)
    newFrame=frame()
    faces(frame=newFrame, pos=vectorList[:len(vectorList)/2], color=PAPER_FRONT_COLOR)
    faces(frame=newFrame, pos=vectorList[len(vectorList)/2:], color=PAPER_BACK_COLOR)
    if PAPER.frame:
        for o in PAPER.frame.objects:
            o.visible=0
    PAPER.frame=newFrame

def partialDraw():
    #redraws a polygon as a component of a larger frame
    #undraw certain triangles and add new ones to the same frame. how?
    return

def drawPoints():
    for i in PAPER.vertices:
        sphere(frame=PAPER.frame, pos=i, radius=30, color=DEFAULT_NODE_COLOR)

def draw():
    drawPolygonSimple()
    drawPoints()

def drawCenter(center):
    drawPolygonCenterSimple(center)
    drawPoints()

def drawCenterOld():
    drawPolygonSimple(True)
    drawPoints()

#-----------------------------------------------------Deformation
def foldSimple(pivots, initPoint):
    m=scene.mouse
    for i in range(0, len(pivots)):
        pivots[i]=pivots[i].pos
    l=pLine(pivots[0], pivots[1])
    totalDis=distP2L(pivots[0], pivots[1], initPoint)
    a=0
    b=0
    for i in range(0,3):
        a+=(pivots[1][i]-pivots[0][i])**2
        b+=(pivots[1][i]-pivots[0][i])*(pivots[0][i]-initPoint[i])
    b*=2
    refVec=vector(l.solvePoint(float(-b)/float(2*a)))
    perp=cross(vector(pivots[0])-refVec, vector(initPoint)-refVec)+refVec
    dragPoint=initPoint
    vList=PAPER.vertices
    while True:
        rate(50)
        try:
            if m.button!='left':#only to raise ValueError
                return
        except ValueError:
            return
        proj=m.project(point=refVec, normal=vector(pivots[0]))
        proj=vector(proj)
        sphere(pos=dragPoint, radius=5)
        for i in range(0, len(vList)):
            if equalVector(dragPoint, vList[i]):
                dragPoint=norm(proj-refVec)*totalDis+refVec
                for j in range(0,3):
                    dragPoint[j]=round(dragPoint[j])
                for v in vList:
                    if equalVector(v, vList[i]) or equalVector(v, pivots[0]) or equalVector(v, pivots[1]):
                        continue
                    if snapAngle(refVec, dragPoint, v)<SNAP_THRESHOLD:
                        print dragPoint
                        for x in range(0, 3):
                            dragPoint[x]=v[x]
                        print dragPoint
                        break
                vList[i]=dragPoint
                break
        drawCenter(refVec)
        #drawCenterOld()
    return

#---------------------------------------------------Miscellaneous
def printVerts(vList):
    for i in vList:
        print'x:',i.x,'y:',i.y,'rad:',polarAngle(i.x, i.y)

def randomNShape(sides):
    if sides<3:
        sides=3
    vList=[vector(randint(-512, 512), randint(-512, 512), 0),vector(randint(-512, 512), randint(-512, 512), 0)]
    i=2
    while i<sides:
        vList+=[vector(randint(-512, 512), randint(-512, 512), 0)]
        i+=1
    return vList

#EXECUTION-------------------------------------------------------
#Note: This declaration was moved because it had to be after class/function definitions.
#Change the shape by changing DEFAULT_SQUARE, same for the AUTOSCALING default.
PAPER=PaperInfo(DEFAULT_SQUARE, None)
drawCenter((0,0,0))
scene.autoscale=AUTOSCALING

if __name__=='__main__':
    while True:
        rate(50)
        if kb.keys:
            key=kb.getkey()
            if key=='ctrl+f':
                select=not select
            if not select:
                for s in pointSelect:
                    s.color=DEFAULT_NODE_COLOR
                pointSelect=[]
        if m.events:
            event=m.getevent()
            if not event.pick:
                continue
            if select and event.pick and event.pick not in pointSelect:
                if event.release=='left' and len(pointSelect)<2:
                    pointSelect+=[m.pick]
                    event.pick.color=SELECT_NODE_COLOR
                if event.drag=='left' and len(pointSelect)==2:
                    if event.pick in pointSelect:
                        continue
                    select=not select
                    #sphere(pos=event.pick.pos, radius=50, color=color.green)
                    foldSimple(pointSelect, event.pick.pos)
                    for s in pointSelect:
                        s.color=DEFAULT_NODE_COLOR
                    pointSelect=[]
