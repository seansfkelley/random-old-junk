# -*- coding: utf-8 -*-
from string import lower
from graphics import *

def replace(string, index, replacement):
    return string[:index]+replacement+string[index+1:]

def leftAndCoeffs(eq):
    if '=' in eq:
        count=0
        while count<len(eq):
            if eq[count]=='=':
                left=eq[:count]
                right=eq[count+1:]
                break
            count+=1
        left=findCoeffs(format(left))
        right=findCoeffs(format(right))
        count=0
        while count<len(left):
            left[count]=left[count]-right[count]
            count+=1
        return left
    return findCoeffs(format(eq))

def format(eq):
    count=0
    while count<len(eq):
        if (ord(eq[count])>64 and ord(eq[count])<91)\
           or (ord(eq[count])>96 and ord(eq[count])<123):
            eq=replace(eq, count, 'x')
            if count==0 or eq[count-1] in '-+':
                eq=replace(eq, count, '1x')
            if count==len(eq)-1 or eq[count+1] in '-+':
                eq=replace(eq, count, 'x1')
        elif eq[count] not in '1234567890-+.':
            eq=replace(eq, count, '')
        elif eq[count] in '1234567890':
            if count==len(eq)-1 and eq[count-1]!='x':
                eq+='x0'
            elif count!=len(eq)-1 and eq[count+1] in '-+' and eq[count-1]!='x':
                eq=replace(eq, count, eq[count]+'x0')
        count+=1
    #if 'x' not in eq or eq[-2]!='x':
        #eq+='x0'
    return eq
    
def findCoeffs(eq):
    print eq
    coeffs=[0,0,0,0]
    count=0
    while count<len(eq):
        if eq[count]=='x':
            temp=eq[:count]
            scount=0
            while scount<len(temp):
                if temp[scount] in '-+':
                    temp=temp[scount+1:]
                    scount=0
                else:
                    scount+=1
            tempIndex=int(count-1-len(temp))
            if tempIndex!=(-1) and eq[tempIndex]=='-':
                coeffs[int(eq[count+1])]-=float(temp)
            else:
                coeffs[int(eq[count+1])]+=float(temp)
        count+=1
    return coeffs

def solveLinear(coeffs):
    return [(coeffs[0]*(-1))/coeffs[1], None, None]

def solveQuadratic(coeffs):
    a,b,c=coeffs[2],coeffs[1],coeffs[0]
    d=(b**2)-(4*a*c)
##    if aa==int(aa):
##        aa=int(aa)
##    if bb==int(bb):
##        bb=int(bb)
##    if dd==int(dd):
##        dd=int(dd)
##    print '('+str(-bb)+'±√'+str(dd)+')/'+str(2*aa)
##    print
    if d>=0:
        return [(-b+d**(1./2))/(2*a), (-b-d**(1./2))/(2*a)]
    return [complex(-b, (-d)**(1./2))/(2*a), complex(-b, -((-d)**(1./2)))/(2*a)]

def solveCubic(coeffs):
    return [None, None, None]

def findRoots(coeffs):
    if coeffs[3]==0:
        if coeffs[2]==0:
            return solveLinear(coeffs)
        return solveQuadratic(coeffs)
    return solveCubic(coeffs)

def solver(eq):##aka display
    roots=findRoots(leftAndCoeffs(eq))
    for i in roots:
        if i!=None:
            if not isinstance(i, complex) and not isinstance(i, string) and i==int(i):
                i=int(i)
            print 'x='+str(i)
    print

##def solver():
##    print 'Enter equation or "q" to quit:'
##    while True:
##        eq=raw_input('')
##        if lower(eq)=='q':
##            break
##        display(eq)

def sin(angleRad):
    result=0
    for n in range(0, 10):
        result+=((-1)**n)*(angleRad**(2.*n+1))/(factorial(2*n+1))
    return round(result, 8)

def cos(angleRad):
    result=0
    for n in range(0, 10):
        result+=((-1)**n)*(angleRad**(2.*n))/(factorial(2*n))
    return round(result, 8)

def tan(angleRad):
    if cos(angleRad)==0:
        return 'inf'
    return round(sin(angleRad)/cos(angleRad), 8)

def csc(angleRad):
    if sin(angleRad)==0:
        return 'inf'
    return round(1/sin(angleRad), 8)

def sec(angleRad):
    if cos(angleRad)==0:
        return 'inf'
    return round(1/cos(angleRad), 8)

def cot(angleRad):
    if sin(angleRad)==0:
        return 'inf'
    return round(cos(angleRad)/sin(angleRad), 8)

def convertToRad(degrees):
    if degrees<0:
        degrees=-(abs(degrees)%360)
        degrees+=360
    else:
        degrees%=360
    return round(degrees*2*pi/360, 8)

def factorial(num):
    result=1
    for i in range(1, num+1):
        result*=i
    return result

def crtWindow(maxX, minX, scaleX, maxY, minY, scaleY, windowSize, xRes, name='Graph'):
    windowSize=round(windowSize, 0)
    window=GraphWin(name, windowSize, windowSize)
    x=abs(round(minX*((windowSize*1.)/(maxX-minX)), 0)) #distance to origin from left side, px
    y=abs(round(maxY*((windowSize*1.)/(maxY-minY)), 0)) #distance to origin from top, px
    if (not (minX>0 or maxX<0)) and x<=windowSize:
        Line(Point(x, 1), Point(x, windowSize)).draw(window)
    elif minX>0:
        x=-abs(x)
    elif maxX<0:
        x=abs(x)
    if (not (minY>0 or maxY<0)) and y<=windowSize:
        Line(Point(1, y), Point(windowSize, y)).draw(window)
    elif minY>0:
        y=-abs(y)
    elif maxY<0:
        y=abs(y)
    pxX=abs(round(windowSize/((maxX-minX)/(scaleX*1.)), 0))
    pxY=abs(round(windowSize/((maxY-minY)/(scaleY*1.)), 0))
    origin=(x,y)
    px=(pxX, pxY)
    dashMarks(window, origin, windowSize, px)
    info='maxX='+str(round(maxX, 3))+' minX='+str(round(minX, 3))+' scaleX='+str(round(scaleX,3))+\
          ' maxY='+str(round(maxY, 3))+' minY='+str(round(minY,3))+' scaleY='+str(round(scaleY,3))+\
          ' xRes='+str(round(xRes,3))
    info=Text(Point(windowSize/2, windowSize-5), info)
    info.setSize(8)
    info.draw(window)
    return (window, px, origin)

def dashMarks(window, origin, windowSize, px):
    windowSize=round(windowSize, 0)
    for i in range(2):
        for j in range(2):
            dash=origin[j]
            while (i==0 and dash<=windowSize) or (i==1 and dash>=0):
                if i==0:
                    dash+=px[j]
                else:
                    dash-=px[j]
                if origin[1-j]==0:
                    if j==0:
                        Line(Point(dash, 1), Point(dash, 4)).draw(window)
                    else:
                        Line(Point(1, dash), Point(4, dash)).draw(window)
                else:
                    if j==0:
                        Line(Point(dash, origin[1]), Point(dash, origin[1]-3)).draw(window)
                    else:
                        Line(Point(origin[0], dash), Point(origin[0]-3, dash)).draw(window)

def newGraph(eq='y=x', preset=None, manual=False, windowSize=400, maxX=1, minX=-1, scaleX=.5, maxY=1, minY=-1, scaleY=.5, xRes=.1):
    if preset!=None:
        windowSize=400
        preset=preset.lower()
        if preset=='trig':
            maxX,minX,scaleX,maxY,minY,scaleY,resX=pi,-pi,pi/4,pi,-pi,pi/4,.01
        elif preset=='unit':
            maxX,minX,scaleX,maxY,minY,scaleY,resX=1,-1,.1,1,-1,.1,.01
        elif preset=='standard':
            maxX,minX,scaleX,maxY,minY,scaleY,resX=10,-10,1,10,-10,1,.1
        elif preset=='i':
            maxX,minX,scaleX,maxY,minY,scaleY,resX=10,0,1,10,0,1,.1
        elif preset=='ii':
            maxX,minX,scaleX,maxY,minY,scaleY,resX=0,-10,1,10,0,1,.1
        elif preset=='iii':
            maxX,minX,scaleX,maxY,minY,scaleY,resX=0,-10,1,0,-10,1,.1
        elif preset=='iv':
            maxX,minX,scaleX,maxY,minY,scaleY,resX=10,0,1,10,-10,1,.1
    temp=crtWindow(maxX, minX, scaleX, maxY, minY, scaleY, windowSize, xRes, eq)
    window=temp[0]
    px=temp[1]
    origin=temp[2]
    size=(maxX, minX, scaleX, maxY, minY, scaleY, xRes)
    return graph(eq, (window, px, origin, size), manual)

def graph(eq, windowInfo, manual=False):
    window=windowInfo[0]
    px=windowInfo[1]
    origin=windowInfo[2]
    size=windowInfo[3]
    maxX=size[0]
    minX=size[1]
    scaleX=size[2]
    maxY=size[3]
    minY=size[4]
    scaleY=size[5]
    xRes=size[6]
    if eq[-2:]=='=y':
        eq=eq[:-2]
    elif eq[:2]=='y=':
        eq=eq[2:]
    coeffs=[0,0,0,0]
    if not manual:
        coeffs=leftAndCoeffs(eq)
    a,b,c,d=coeffs[3],coeffs[2],coeffs[1],coeffs[0]
    x=0
    points=[]
    count=0
    while x<=maxX:
        y=a*x**3+b*x**2+c*x+d
        if manual:
            y=tan(x)
        #if y<maxY and y>minY:
        points+=[Point(origin[0]+(x*px[0]/(scaleX*1.)), origin[1]-(y*px[1]/(scaleY*1.)))]
        x+=xRes
        count+=1
    x=0
    while x>=minX:
        y=a*x**3+b*x**2+c*x+d
        if manual:
            y=tan(x)
        #if y<maxY and y>minY:
        points=[Point(origin[0]+(x*px[0]/(scaleX*1.)), origin[1]-(y*px[1]/(scaleY*1.)))]+points
        x-=xRes
        count+=1
    lines=[]
    i=0 
    while i<len(points)-1:
        temp=Line(points[i], points[i+1])
        #temp.setColor('blue')
        temp.draw(window)
        i+=1
    return (window, px, origin, size)

def help():
    print 'Help topics:'
    print '  1. General'
    print '  2. Equation Solver'
    print '  3. Grapher'
    print '  4. Advanced Grapher'
    print '  5. Other'
    print '  6. Close help'
    while True:
        x=input()
        if x==1:
            print 'When asked for an equation or keyword, always enter it inside'
            print 'quotes (""), according to the following rules:'
            print '  -one variable per equation'
            print '  -exponents: xa, where x is the variable and a is the power,'
            print '     do not use x^a'
            print '  -no parenthesis'
            print '  -no other extraneous characters'
        elif x==2:
            print 'Start the equation solver by typing "solver(x)". x is your'
            print 'equation, entered with the syntax described in General help.'
            print 'The appropiate soultion method is automatically taken.'
            print 'The variable is always converted into x, regardless of the'
            print 'original, one variable per equation.'
        elif x==3:
            print 'Create a new graph with "newGraph(x, y)" where x is your'
            print '"y=" equation in correct syntax, and y is a preset keyword.'
            print 'Preset keywords are a shortcut for setting the window size:'
            print '  -"trig" - 4-quadrants, pi each direction, pi/4 scale'
            print '  -"unit" - 4 quadrants, 1 each direction, .1 scale'
            print '  -"standard" - 4 quadrants, 10 each direction, 1 scale'
            print '  -"i", "ii", "iii", "iv" - 1 quadrant, 10 by 10 of the'
            print '     corresponding quadrant, 1 scale'
            print
            print 'If you plan to superimpose more graphs in the same window'
            print 'set a variable to newGraph(), like so: "var=newGraph()".'
            print 'When you want to put more lines in this window, use the'
            print 'graph(x, y) function, where x is the equation you want to'
            print 'graph and y is the variable from newGraph().'
        elif x==4:
            print 'If you want to create a graph to your own specifications,'
            print 'set preset to None, and put them in this order:'
            print '  -maxX: max x value displayed in the window'
            print '  -minX: min x value displayed in the window'
            print '  -scaleX: space between scale marks on the x-axis'
            print '  -maxY, minY, scaleY: same as corresponding x inputs'
            print '  -xRes: the accuracy of the graph, i.e. x distance between'
            print '     points'
            print
            print 'Code for more complex equations that the equation solver cant'
            print 'solve can be manually input into the program code in the'
            print 'specified place, this is mostly used for trigonomatric graphs.'
            print 'The arguement manual should be set to True when doing this.'
        elif x==5:
            print 'This program also comes with all the trigonometric functions,'
            print 'sin, cos, tan, csc, sec, cot.'
        else:
            break

pi=3.14159265

print 'Type "help()" for information on this program.'

#newGraph('y=x2', 10, -10, 2, 100, 0, 10, .1, 400)  #parabola
#newGraph('y=tan(x)', 'trig', True)                 #tan
