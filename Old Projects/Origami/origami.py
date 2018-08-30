#INDEX-----------------------------------------------------------
 #CONSTANTS/IMPORTS
 #VARIABLES
 #CLASSES
 #FUNCTIONS
  #Mathematical
  #Drawing
  #Interaction
  #Hotkeys
  #Test/Miscellaneous
 #EXECUTION
 #NOTES

#CONSTANTS/IMPORTS-----------------------------------------------
from visual import *
from random import randint
from time import sleep
from math import sqrt
MACHINE_ERROR=10**-9
DEFAULT_VERT_COLOR=(.5,.5,.5)
SELECT_VERT_COLOR=(.7,.7,.7)
FIXED_VERT_COLOR=(1,.3,.3)
FIXED_SELECT_VERT_COLOR=(1,.5,.5)
PAPER_FRONT_COLOR=(0,.6,0)
PAPER_BACK_COLOR=(.6,.6,.6)
CREASE_COLOR=(0,.5,0)
ARROW_COLOR=(.5,.5,.5)
VERT_SIZE=30
CREASE_RADIUS=2
ARROW_WIDTH=10
SNAP_THRESHOLD=math.pi/12
AUTOSCALING=0
PAPER_SIDE_LEN=1024
PAPER=None
HOTKEYS=None
DRAG_ACTIONS=None
FRAME=frame()
TITLE_DEFAULT="Origami - No Action Selected"
TITLE_HEAD_CUR="Origami - Current Action: "
TITLE_HEAD_PRE="Origami - Previous Action: "
#PAPER, HOTKEYS, DRAG_ACTIONS under Execution

#VARIABLES-------------------------------------------------------
scene.ambient=.6
m=scene.mouse
kb=scene.kb
canSelect=False
selectedVerts=[]
currentAction=None
numVertsReq=-1
undoStack=[]
redoStack=[]
fixedPoints={}
hashCounter=0
epo=None
creaseLines={}

#CLASSES---------------------------------------------------------
class PaperInfo:
    def __init__(self, vertices=None, tris=None, vertDictionary=None):
        if vertices:
            self.verts=vertices
        else:
            self.verts=[]
        if tris:
            self.triangles=tris
        else:
            self.triangles=[]
        if vertDictionary:
            self.vertDict=vertDictionary
        else:
            self.vertDict={}
    def __getitem__(self, key):
        return self.verts[key]
    def __setitem__(self, key, value):
        del self.vertDict[self[key]]
        self.vertDict[value.hash]=value
        self.verts[key]=value
    def __add__(self, other):
        return self.__concat__(other)
    def __iadd__(self, other):
        return self.__concat__(other)
    def __concat__(self, other):
        for v in other:
            self.vertDict[v.hash]=v
        return PaperInfo(self.verts+other, self.triangles, self.vertDict)
    def __iconcat__(self, other):
        return self.__concat__(other)
    def __delitem__(self, value):
        self.verts.remove(value)
        del self.vertDict[value.hash]
    def __len__(self):
        return len(self.verts)
    def __str__(self):
        if not self.verts:
            return 'PaperInfo: []'
        temp='['
        for v in self:
            temp+=str(vector(v.coords))+', '
        return 'PaperInfo: '+temp[:-2]+']'
    def __iter__(self):
        for v in self.verts:
            yield v
        return
    def constructDictionary(self):
        vertDict={}
        for v in self:
            vertDict[v.hash]=v

class Triangle:
    def __init__(self, v1, v2, v3):
        #these verts are the actual Vertex objects also found in PaperInfo
        self.verts=[v1, v2, v3]
        self.face=None
        self.backface=None
        if findNormal(vector(v1), vector(v2), vector(v3))[2]<0:
            self.verts[0], self.verts[2]=self.verts[2], self.verts[0]
    def __contains__(self, v):
        return equalVector(self[0], v) or\
               equalVector(self[1], v) or\
               equalVector(self[2], v)
    def __eq__(self, other):
        return self[0] in other and\
               self[1] in other and\
               self[2] in other and\
               other[0] in self and\
               other[1] in self and\
               other[2] in self
    def __getitem__(self, key):
        return self.verts[key]
    def __iter__(self):
        yield self[0]
        yield self[1]
        yield self[2]
        return
    def __str__(self):
        return 'Triangle<'+str(self[0])+', '+str(self[1])+', '+str(self[2])+'>'
    def initialize(self):
        global creaseLines
        self.face=faces(pos=self.facesList(), color=PAPER_FRONT_COLOR)
        self.backface=faces(pos=self.backsideAsList(), color=PAPER_BACK_COLOR)
        for v in self.verts:
            v.triangles+=[self]
        for i in range(3):
            one=self[i]
            two=self[(i+1)%3]
            if creaseLines.has_key(str(one.hash)+':'+str(two.hash)) or\
               creaseLines.has_key(str(two.hash)+':'+str(one.hash)):
                continue
            creaseLines[str(one.hash)+':'+str(two.hash)]=\
                cylinder(pos=vector(one.coords), axis=vector(two.coords)-vector(one.coords),
                         color=CREASE_COLOR, radius=CREASE_RADIUS)
    def facesList(self):
        return [list(self[0]), list(self[1]), list(self[2])]
    def area(self):
        #S = |AB x AC|/2
        #problem: returns double the value even counting the 1/2
        return .5*mag(cross(vector(self[0])-vector(self[1]),
                            vector(self[0])-vector(self[2])))
    def backsideAsList(self):
        return [list(self[2]), list(self[1]), list(self[0])]
    def redraw(self):
        self.face.pos=self.facesList()
        self.backface.pos=self.backsideAsList()
        for i in range(3):
            one=self[i]
            two=self[(i+1)%3]
            try:
                temp=creaseLines[str(one.hash)+':'+str(two.hash)]
                temp.pos=vector(one.coords)
                temp.axis=vector(two.coords)-temp.pos
            except KeyError:
                temp=creaseLines[str(two.hash)+':'+str(one.hash)]
                temp.pos=vector(two.coords)
                temp.axis=vector(one.coords)-temp.pos
    def destroy(self):
        for v in self.verts:
            v.triangles.remove(self)
        PAPER.triangles.remove(self)
        self.face.visible=0
        self.backface.visible=0

class Vertex:
    def __init__(self, x, y, z):
        global hashCounter
        self.coords=vector(x, y, z)
        self.alt=vector(self.coords)#different object from coords
        self.knex=[]
        self.triangles=[]
        self.hash=hashCounter
        self.attached=[]
        self.sp=sphere(pos=vector(self.coords), radius=VERT_SIZE, color=DEFAULT_VERT_COLOR)
        self.sp.owner=self
        self.arrows={}
        hashCounter+=1
    def __getitem__(self, key):
        return self.coords[key]
    def __setitem__(self, key, value):
        self.coords[key]=value
    def __str__(self):
        #csv=comma separated values
        #syntax: coords(csv);alt coords(csv);knex hashes(csv);attached hashes(csv);fixed status(t/f);hash value \n
        string=''
        for i in range(3):
            string+=str(self[i])+','
        string=string[:-1]+';'
        for i in range(3):
            string+=str(self.alt[i])+','
        string=string[:-1]+';'
        for v in self.knex:
            string+=str(v.hash)+','
        string=string[:-1]+';'
        for v in self.attached:
            string+=str(v.hash)+','
        string=string[:-1]+';'
        if not self.attached:
            string+=';'
        if self in fixedPoints:
            string+='1'
        else:
            string+='0'
        string+=';'
        string+=str(self.hash)
        return string
    def __len__(self):
        return 3
    def __eq__(self, other):
        return self.hash==other.hash
    def __hash__(self):
        return self.hash
    def __cmp__(self,other):
        return self.hash-other.hash
    def changeHash(self, newHash):
        #use only if sure this will not cause hash collisions
        del PAPER.vertDict[self]
        self.hash=newHash
        PAPER.vertDict[self]=self
    def setColor(self):
        i=int(self in selectedVerts)
        i+=2*int(self in fixedPoints)
        self.sp.color=(DEFAULT_VERT_COLOR, SELECT_VERT_COLOR, FIXED_VERT_COLOR, FIXED_SELECT_VERT_COLOR)[i]
    def move(self, newCoords, stationary=None):
        if stationary:
            stationary=list(stationary)
        else:
            stationary=[]
        stationary+=list(fixedPoints)#create a copy
        self.moveRecurse(newCoords, stationary)
    def moveRecurse(self, newCoords, alreadyMoved):
        self.sp.pos=self.coords=vector(newCoords)
        for a in self.attached:
            a=a[0]
            self.arrows[a].pos=self.coords
            self.arrows[a].axis=a.coords-self.coords
            a.arrows[self].pos=a.coords
            a.arrows[self].axis=self.coords-a.coords
        for t in self.triangles:
            t.redraw()
        alreadyMoved+=[self]
        for mover in self.knex:
            if mover in alreadyMoved:
                continue
            if abs(distP2P(self, mover)-distP2P(self.alt, mover.alt))>MACHINE_ERROR:
                points=list(mover.knex)
                points.remove(self)
                radii=[]
                for v in self.attached:
                    points=[v[0]]+points
                    radii=[v[1]]+radii
                points=points[:2]+[self]#need to guarentee that self is in the list (force it to move)
                i=len(radii)
                while i<3:
                    radii+=[distP2P(points[i].alt, mover.alt)]
                    i+=1
                result=trilaterate(points, radii)
                if result==None:
                    continue
                mover.moveRecurse(result, alreadyMoved)
    def attach(self, other):
        if other in self.knex:
            print "Points already connected."
            return
        if len(self.attached)==2 or len(other.attached)==2:
            print "Too many attachments."
            return
        self.attached+=[[other, distP2P(self, other)]]
        other.attached+=[[self, distP2P(self, other)]]
        self.arrows[other]=arrow(pos=vector(self.coords), axis=vector(other.coords-self.coords),
                                 shaftwidth=ARROW_WIDTH, color=ARROW_COLOR)
        self.arrows[other].fixedwidth=1
        other.arrows[self]=arrow(pos=vector(other.coords), axis=vector(self.coords-other.coords),
                                 shaftwidth=ARROW_WIDTH, color=ARROW_COLOR)
        other.arrows[self].fixedwidth=1
    def detach(self, other):
        for v in self.attached:
            if v[0] is other:
                self.attached.remove(v)
        for v in other.attached:
            if v[0] is self:
                other.attached.remove(v)
        self.arrows[other].visible=0
        del self.arrows[other]
        other.arrows[self].visible=0
        del other.arrows[self]
    def destroy(self):
        for v in self.knex:
            v.knex.remove(self)
        for v in self.attached:
            self.detach(v)
        del PAPER.vertDict[self]
        PAPER.verts.remove(self)
        for t in list(self.triangles):
            t.destroy()
        self.sp.visible=0

class Line:
    def __init__(self, point1, point2):
        self.points=(vector(point1), vector(point2))
        self.dirVec=norm(self[1]-self[0])#normalized direction of line from point1, direction vector
    def __getitem__(self, key):
        return self.points[key]
    def __contains__(self, point):
        return self.onLine(point)
    def onLine(self, point):
        if equalVector(point, self[0]) or equalVector(point, self[1]):
            return True
        return parallelVec(self.dirVec, vector(point)-self[0])
    def solvePoint(self, dist):
        return dist*self.dirVec+self[0]
    def intersection(self, other):
        #http://mathforum.org/library/drmath/view/62814.html
        #L1 = P1 + a V1 and L2 = P2 + b V2
        #a (V1 X V2) = (P2 - P1) X V2
        vec1, vec2 = cross(self.dirVec, other.dirVec), cross(other[0]-self[0], other.dirVec)
        #dont quite understand: are both these checks needed, or are they redundant?
        if not parallelVec(vec1, vec2) or isZero(vec1):
            return None
        return (mag(vec2)/mag(vec1))*self.dirVec+self[0] #plug back into first line equation
    def vertsOnLine(self):
        temp=[]
        for v in PAPER:
            if self.onLine(v):
                temp+=[v]
        return temp
    def distToPoint(self, point):
        AB=self[1]-self[0]
        AP=vector(point)-self[0]
        return abs(mag(cross(AP, AB))/mag(AB))

class UserAction:
    def __init__(self, act, ptsReq, titleTail, selectable=True):
        self.select=selectable
        self.action=act
        self.vertsReq=ptsReq
        self.title=titleTail
    def go(self):
        global canSelect, currentAction, numVertsReq
        canSelect=self.select
        currentAction=self.action
        numVertsReq=self.vertsReq
        scene.title=TITLE_HEAD_CUR+self.title
        resetSelection()

class ImmediateAction:
    def __init__(self, act, titleTail):
        self.action=act
        self.title=titleTail
    def go(self):
        self.action()
        #scene.title=TITLE_HEAD_PRE+self.title
        
#FUNCTIONS-------------------------------------------------------

#----------------------------------------------------Mathematical
def equalVector(v1, v2):
    for i in range(3):
        if abs(v1[i]-v2[i])>MACHINE_ERROR:
            return False
    return True

def parallelVec(v1, v2):
    return equalVector(norm(v1), norm(v2))

def distP2P(p1, p2):
    return abs(mag(vector(p2)-vector(p1)))

def collinear(pointList):
    l=Line(pointList[0], pointList[1])
    for i in range(2, len(pointList)):
        if pointList[i] not in l:
            return False
    return True

def orderLinearPoints(points, start, end):
    #puts points in order from start to end, regardless of their knex status
    if start not in points:
        points+=[start]
    if end not in points:
        points+=[end]
    return sorted(points, lambda x,y: int(distP2P(start, x)-distP2P(start,y)))

def linearPath(start, end):
    #lists points, in order, that make up a connection from start to end
    allPoints=Line(start, end).vertsOnLine()
    return linearHelper([], start, end, allPoints)

def linearHelper(path, current, target, choices):
    path+=[current]
    choices.remove(current)
    if current is target:
        return path
    for k in current.knex:
        if k in choices:
            return linearHelper(path, k, target, choices)
    return []
                
def findNormal(plane1, plane2, plane3):
    #n = (b - a) x (c - a)
    return norm(cross((plane2-plane1),(plane3-plane1)))

def isZero(vec):
    return equalVector(vec, (0,0,0))

def angleCCW(compAxis, rotAxis, vec, ang):
    if not equalVector(norm(rotate(vector(vec), angle=ang, axis=rotAxis)), compAxis):
        return 2*math.pi-ang
    return ang

def vertAtPosition(pos):
    for v in PAPER:
        if equalVector(v, pos):
            return v
    return None

def trilaterate(pts, radii):
    displace=vector(pts[0])
    p1, p2, p3 = vector(pts[0]), vector(pts[1]), vector(pts[2])
    r1, r2, r3 = float(radii[0]), float(radii[1]), float(radii[2])
    #shift points to fit conditions: one origin, one x-axis, one xy plane
    p2-=p1
    p3-=p1
    p1=vector(0,0,0)
    angles=[]
    for (compAxis, rotAxis, vec) in ((vector(1,0,0), (0,0,1), vector(p2[0], p2[1], 0)),
                                     (vector(1,0,0), (0,1,0), vector(p2[0], 0, p2[2])),
                                     (vector(0,1,0), (1,0,0), vector(0, p3[0], p3[1]))):
        angles+=[angleCCW(compAxis, rotAxis, vec, compAxis.diff_angle(vec))]
        p2=rotate(p2, angle=angles[-1], axis=rotAxis)
        p3=rotate(p3, angle=angles[-1], axis=rotAxis)
    XYangle, XZangle, YZangle = angles
    #en.wikipedia.org/wiki/Trilateration
    x=(r1**2-r2**2+p2[0]**2)/(2*p2[0])
    y=(r1**2-r3**2+p3[0]**2+p3[1]**2)/(2*p3[1]) - (p3[0]*x)/p3[1]
    if abs(x)<MACHINE_ERROR:
        x=0.0
    if abs(y)<MACHINE_ERROR:
        y=0.0
    z=r1**2-x**2-y**2
    if abs(z)<MACHINE_ERROR:
        z=0.0
    if z<0:
        return None
    z=math.sqrt(z)
    results=[vector(x,y,z)]
    if z!=0:
        results+=[vector(x, y, -z)]
    #undo rotations/translation
    for (ang, ax) in ((-YZangle, (1,0,0)),
                      (-XZangle, (0,1,0)),
                      (-XYangle, (0,0,1))):
        for i in range(len(results)):
            results[i]=rotate(results[i], angle=ang, axis=ax)
    for i in range(len(results)):
        results[i]+=displace
    #pts, rad index 2 are the moving point (see vertex.move)
    if abs(distP2P(results[0], pts[2])-radii[2])>MACHINE_ERROR:
        return results[1]
    return results[0]

#---------------------------------------------------------Drawing
def calcTriangles():
    global creaseLines
    creaseLines={}
    for t in PAPER.triangles:
        t.face.visible=0
        t.backface.visible=0
    PAPER.triangles=[]
    for v in PAPER:
        v.triangles=[]
    for one in PAPER:
        for two in one.knex:
            for three in two.knex:
                if one in three.knex:
                    temp=Triangle(one, two, three)
                    if temp.area()!=0 and not alreadyDrawn(temp):
                        PAPER.triangles+=[temp]
                        temp.initialize()
                    break

def alreadyDrawn(triangle):
    for t in PAPER.triangles:
        if triangle==t:
            return True
    return False

#-----------------------------------------------------Interaction
def foldPivots(points):
    pivot0, pivot1, dragPoint=points[0].coords, points[1].coords, points[2].coords
    pivotLine=Line(pivot0, pivot1)
    pivotLinePts=linearPath(points[0], points[1])
    if dragPoint in pivotLine or not pivotLinePts:
        #cannot define the normal if the points form a line or
        #if the points arent connected directly or indirectly in a straight line
        return
    vertex=points[2]
    originalPos=vector(vertex)
    totalDis=pivotLine.distToPoint(dragPoint)
    #http://www.geocities.com/SiliconValley/2151/math3d.html (intersection sphere/line)
    #Line equation: p = org + (-B/2A) * dir
    #A = dir^2 
    #B = 2 * dir * (lineOrg-sphOrg) 
    a=dot(pivotLine.dirVec, pivotLine.dirVec)
    b=2*dot(pivotLine.dirVec, (pivotLine[0]-originalPos))
    rotationCenter=pivotLine.solvePoint(-b/(2*a))
    nor=norm(vector(pivot0)-rotationCenter)
    while True:
        rate(50)
        try:
            if m.button!='left':
                addUndo(('move', vertex, originalPos))
                return
        except ValueError:
            addUndo(('move', vertex, originalPos))
            return
        proj=vector(m.project(normal=nor, point=rotationCenter))
        dragPoint=norm(proj-rotationCenter)*totalDis+rotationCenter
        vertex.move(dragPoint, pivotLinePts)

def foldCenRad(points):
    center, radius, dragPoint=points[0].coords, points[1].coords, points[2].coords
    if collinear([center, radius, dragPoint]):
        return
    vertex=points[2]
    originalPos=vector(vertex)
    totalDis=distP2P(center, dragPoint)
    nor=norm(findNormal(center, radius, dragPoint))
    while True:
        rate(50)
        try:
            if m.button!='left':
                addUndo(('move', vertex, originalPos))
                return
        except ValueError:
            addUndo(('move', vertex, originalPos))
            return
        proj=vector(m.project(point=center, normal=nor))
        dragPoint=norm(proj-center)*totalDis+center
        vertex.move(dragPoint)

def makeMidpoint(points):
    insertPoint(points, .5*distP2P(points[0], points[1]))
    
def insertPoint(points, distance):
    global PAPER
    pt1, pt2=points
    try:
        pt1.knex.remove(pt2)
        pt2.knex.remove(pt1)
    except ValueError: #they are not connected
        return
    point=Line(pt1, pt2).solvePoint(distance)
    point=Vertex(point[0], point[1], point[2])
    PAPER+=[point]
    point=Line(pt1.alt, pt2.alt).solvePoint(distance)
    PAPER[-1].alt=point
    point=PAPER[-1]
    point.knex=[pt1, pt2]
    for v in pt1.knex:
        if v in pt2.knex:
            point.knex+=[v]
            v.knex+=[point]
    pt1.knex+=[point]
    pt2.knex+=[point]
    temp=list(pt1.triangles)#a list holding the same elements is made, the original list is to be changed
    for t in temp:
        if pt2 in t:
            for v in t:
                if v is pt1 or v is pt2:
                    continue
                t.destroy()
                tri1, tri2=Triangle(pt1, v, point), Triangle(pt2, v, point)
                tri1.initialize()
                tri2.initialize()
                PAPER.triangles+=[tri1, tri2]
    addUndo(('insert', point, pt1, pt2))

def makeCrease(points):
    #use alts. draw lines of crease, use creaseList to check for intersections
    #of alt-lines then create verts and make connections
    #can interesct at any point on line, even one that isnt part of that segment - to avoid
    #make sure distance from the endpoints is not greater than the dist between endpoints
    #use linearPath to find four points on the lines nearest the intersection
    #how to handle passes through existing points?
    pt1, pt2=points
    crease=Line(pt1.alt, pt2.alt)
    possibleLines=creaseLines.keys()
    intersections=[]
    for line in possibleLines:
        line=line.split(':')
        endPts=[0]*2
        endPts[0], endPts[1]=PAPER.vertDict[int(line[0])], PAPER.vertDict[int(line[1])]
        line=Line(endPts[0].alt, endPts[1].alt)
        intersect=crease.intersection(line)
        if not intersect:
            continue
        dist0, dist1=distP2P(intersect, line[0]), distP2P(intersect, line[1])
        if abs(distP2P(line[0], line[1])-dist0-dist1)>MACHINE_ERROR:
            #doesnt fall on the segment of the line between the points
            continue
        intersections+=[[endPts[0], endPts[1], dist0]]
        if dist0<MACHINE_ERROR:
            #equal to first endpoint of the segment
            intersections[-1]+=[0]
        elif dist1<MACHINE_ERROR:
            #other endpoints
            intersections[-1]+=[1]
        else:
            #is at some other point on the segment
            intersections[-1]+=[-1]
    #intersections element syntax: [segment end0, segment end1, dist from seg0, equal to endpoint#]
    creaseVerts=[]
    for pointInfo in intersections:
        if pointInfo[3]!=-1:
            if pointInfo[pointInfo[3]] not in creaseVerts:
                creaseVerts+=[pointInfo[pointInfo[3]]]
        else:
            insertPoint(pointInfo[:2], pointInfo[2])
            creaseVerts+=[PAPER[-1]]
    creaseVerts=orderLinearPoints(creaseVerts, pt1, pt2)
    for i in range(len(creaseVerts)-1):
        creaseVerts[i].knex+=[creaseVerts[i+1]]
        creaseVerts[i+1].knex+=[creaseVerts[i]]
    calcTriangles()

def fixPoint(points):
    global fixedPoints
    point=points[0]
    if point in fixedPoints:
        fixedPoints.remove(point)
    else:
        fixedPoints+=[point]
    point.setColor()

def attachPoints(points):
    points[0].attach(points[1])

#---------------------------------------------------------Hotkeys
def printCommands():
    print "\nCommands:"
    for k in HOTKEYS.keys():
        print k+": "+HOTKEYS[k].title

def resetSelection():
    global selectedVerts
    while selectedVerts:
        temp=selectedVerts[0]
        selectedVerts.remove(temp)
        temp.setColor()

def unfixAllPoints():
    global fixedPoints
    for v in fixedPoints:
        v.setColor()
    fixedPoints=[]

def reset():
    global canSelect, numVertsReq
    canSelect=False
    resetSelection()
    numVertsReq=-1
    unfixAllPoints()
    scene.title=TITLE_DEFAULT

def addUndo(action):
    global redoStack
    undoStack.append(action)
    redoStack=[]

def undo():
    try:
        action=undoStack.pop()
    except IndexError:
        return
    if action[0]=='move':
        #('move', vertex, originalPosition)
        temp=vector(action[1])
        action[1].move(action[2])
        redoStack.append(('move', action[1], temp))
    elif action[0]=='mdpt':
        #('mdpt', midpoint, point1, point2)
        others=list(action[1].knex)
        others.remove(action[2])
        others.remove(action[3])
        action[1].destroy()
        if len(others)==2:
            PAPER.triangles+=[Triangle(action[2], action[3], others[1])]
            PAPER.triangles[-1].initialize()
        PAPER.triangles+=[Triangle(action[2], action[3], others[0])]
        PAPER.triangles[-1].initialize()
        action[2].knex+=[action[3]]
        action[3].knex+=[action[2]]
        redoStack.append(('mdpt', action[2], action[3]))

def redo():
    global redoStack
    try:
        action=redoStack.pop()
    except IndexError:
        return
    if action[0]=='move':
        #('move', vertex, originalPosition)
        temp=vector(action[1])
        action[1].move(action[2])
        undoStack.append(('move', action[1], temp))
    elif action[0]=='mdpt':
        #('mdpt', point1, point2)
        temp=list(redoStack)
        makeMidpoint(action[1:])
        redoStack=temp

#----------------------------------------------Test/Miscellaneous
def save():
    name=raw_input('Filename? ')
    exists=True
    try:
        f=open(name+'.ori', 'r')
    except IOError:
        exists=False
    if exists:
        print 'File exists. Replace [Y/N]?',
        over=''
        while over!='y' and over!='n':
            over=raw_input('').lower()
        if over=='n':
            print 'Save cancelled.'
            return
    f=open(name+'.ori', 'w')
    for v in PAPER:
        f.write(str(v)+'\n')
    f.close()
    print 'Save successful!'

def load(filename='origami.ori'):
    global PAPER
    PAPER=PaperInfo()
    for o in scene.objects:
        o.visible=0
    f=open(filename, 'r')
    for line in f:
        line=line.split(';')
        #csv=comma separated values
        #syntax: coords(csv);alt coords(csv);knex hashes(csv);attached hashes(csv);fixed status(t/f);hash value\n
        temp=line[0].split(',')
        PAPER+=[Vertex(float(temp[0]), float(temp[1]), float(temp[2]))]
        v=PAPER[-1]
        temp=line[1].split(',')
        v.alt=vector(float(temp[0]), float(temp[1]), float(temp[2]))
        temp=line[2].split(',')
        v.knexHashesTemp=[]
        for h in temp:
            v.knexHashesTemp+=[int(h)]
        temp=line[3].split(',')
        v.attachedHashesTemp=[]
        if(temp[0]):#if there are attached ones
            for h in temp:
                v.attachedHashesTemp+=[int(h)]
        if int(line[4]):
            fixedPoints+=[v]
        v.changeHash(int(line[5][:-1]))
        v.setColor()
    f.close()
    for v in PAPER:
        v.knex=[]
        for k in v.knexHashesTemp:
            v.knex+=[PAPER.vertDict[k]]
        for a in v.attachedHashesTemp:
            v.attached+=[PAPER.vertDict[a]]
    global hashCounter
    hashCounter=max(PAPER).hash+1
    calcTriangles()
    print filename+': load successful!'

def showNormals(points):
    p=[0]*3
    for i in range(3):
        p[i]=points[i].coords
    arrow(pos=(0,0,0), axis=findNormal(p[0], p[1], p[2])*128, shaftwidth=25, frame=FRAME)
    waitAndErase(3)
        
def showKnex():
    global m
    epo=None
    while True:
        rate(50)
        if m.events:
            event=m.getevent()
            if not event.pick or event.release!='left':
                continue
            lastEpo=epo
            epo=event.pick.owner
            waitAndErase(0)
            if lastEpo is epo:
                return
            for v in epo.knex:
                arrow(pos=epo.coords, axis=v.coords-epo.coords, shaftwidth=25, frame=FRAME)

def showAllKnex():
    for v in PAPER:
        for k in v.knex:
            arrow(pos=v, axis=k.coords-v.coords, shaftwidth=25, frame=FRAME)
    waitAndErase(5)

def waitAndErase(howLong):
    sleep(howLong)
    for o in FRAME.objects:
        if isinstance(o, arrow):
            o.visible=0

#EXECUTION-------------------------------------------------------
def initializePaper():
    global PAPER
    PAPER=PaperInfo()
    for (x, y) in ((-1, 1), (1, 1), (1, -1), (-1, -1)):
        PAPER+=[Vertex(PAPER_SIDE_LEN/2*x, PAPER_SIDE_LEN/2*y, 0)]
    for i in range(4):
        PAPER[i].knex=[PAPER[i-1], PAPER[(i+1)%4]]
    PAPER+=[Vertex(0, 0, 0)]
    for i in range(4):
        PAPER[-1].knex+=[PAPER[i]]
        PAPER[i].knex+=[PAPER[-1]]
    for i in range(4):
        makeMidpoint([PAPER[i], PAPER[(i+1)%4]])
    calcTriangles()

def initialize():
    #functions need to be defined before they can be put in these lists
    #scene.lights+=[norm(vector(1,1,1))*.7]
    
    global HOTKEYS
    HOTKEYS={'ctrl+d':ImmediateAction(resetSelection, "Deselect All"),
             'ctrl+r':ImmediateAction(reset, "Reset All Points"),
             'ctrl+m':UserAction(makeMidpoint, 2, "Create Midpoint"),
             'ctrl+c':UserAction(makeCrease, 2, "Create Crease"),
             'ctrl+a':UserAction(attachPoints, 2, "Attach Points"),
             'ctrl+z':ImmediateAction(undo, "Undo"),
             'ctrl+y':ImmediateAction(redo, "Redo"),
             'ctrl+x':UserAction(fixPoint, 1, "Fix Point"),
             'ctrl+shift+x':ImmediateAction(unfixAllPoints, "Unfix All Points"),
             'ctrl+q':UserAction(foldPivots, 2, "Folding by Pivot Line"),
             'ctrl+w':UserAction(foldCenRad, 2, "Folding by Center-Radius"),
             'ctrl+h':ImmediateAction(printCommands, "Show Commands"),
             'ctrl+s':ImmediateAction(save, "Save"),
             'ctrl+o':ImmediateAction(load, "Open"),
             #DEBUG COMMANDS
             'ctrl+n':UserAction(showNormals, 3, "DEBUG - Show Normals"),
             'ctrl+k':ImmediateAction(showKnex, "DEBUG - Show Knex"),
             'ctrl+shift+k':ImmediateAction(showAllKnex, "DEBUG - Show All Knex")}

    global DRAG_ACTIONS
    DRAG_ACTIONS=(foldPivots, foldCenRad)

#NOTES-----------------------------------------------------------

#for fold:
    #snap
    #check for illegal folds
#how to use stacked vertices?
#add ctrl z, ctrl y for all new actions
#triangle surface area can easily be used for error-checking - but how to use it for finding points?
#creases -> sometimes triangles disappear, also dont use calcTriangle,s figure out what needs refreshing
#restrict creases to between the endpoints - sometimes they go outside bounds
#trilaterate: priority to certain points (already moved, attached and already moved, etc), if less
#than 3 skip and come back later

if __name__=='__main__':
    initialize()
    initializePaper()
    scene.autoscale=AUTOSCALING
    undoStack=[]#adding midpoints adds to the stack in initialize!
    print "Type ctrl+h for command list."
    scene.title=TITLE_DEFAULT
    while True:
        rate(50)
        if kb.keys:
            try:
                HOTKEYS[kb.getkey()].go()
            except KeyError:
                pass
        if m.events:
            event=m.getevent()
            if not event.pick or event.pick.__class__ is not sphere:
                continue
            if canSelect:
                epo=event.pick.owner
                if event.release=='left':
                    if epo in selectedVerts:
                        selectedVerts.remove(epo)
                        epo.setColor()
                        continue
                    if len(selectedVerts)<numVertsReq:
                        selectedVerts+=[epo]
                        epo.setColor()
                        if len(selectedVerts)==numVertsReq and currentAction not in DRAG_ACTIONS:
                            currentAction(selectedVerts)
                            resetSelection()
                if event.drag=='left' and len(selectedVerts)==numVertsReq and\
                   currentAction in DRAG_ACTIONS and epo not in selectedVerts:
                    currentAction(selectedVerts+[epo])
                    resetSelection()
                if event.release=='right':
                    pass
