# -*- coding: cp1252 -*-
#fraction solver wih LCM + - * / (how to with variables?)
#R/T/D solver (default parameters)
#absoulte value should isolate the || statement. moveleft, solve the
#linear/quadratic/cubic remaining, multiply right side by -1 and then repeat
#2, 4, or 6 answers. only accept linears for inequalities (also do imag)
#factor will say non-factorable if the variable has a coeff: (x+2)(x-2) can be returned
#but if the answer is (2x+2)(x-2) it will say non-factorable
#imaginary numbers possible for equation() (all 3 types) (complex numbers)
#for all instances of cuberoot and sqrt, round to 3 digits
#simplify does nothing, prints zeores
#remainder support for division
# complex number and fraction support (classes)
#graph support for equations (slope, x-int, y-int) new func: graphs(eq="")
#allow use of y variable in those (adapt stringsetup to have a bool that if true
#will alow use of y)
#plugin(eq="") function
#if findcoeffs always put in axb (ex: x -> 1x1, 2 -> 2x0), triplenegative
#could be used
#reformat equation answer with {}

import math
import copy
print "Functions: equation solver/multiplier/divider - solver(), equation factoerer -"
print "factor(), absolute value (in)equalities - absolute(), LCM - lcm(), GCF - gcf(),"
print "factor out GCF from numbers - simplify(), square roots - sqrt(), help - help()."

def help(function=""):
    if function=="":
        function=raw_input("Enter function name or 'general': ")
    function=lowercase(function)
    print
    if function=="general":
        print "This is the algebra solver. It encompasses all the functions"
        print "listed above. The variable used does not matter, although"
        print "the functions will always return the variable as 'x'. When"
        print "writing terms with an exponent, write the term as axb, where"
        print "a is the coeffecient (no coeffecient defaults to 1), x is"
        print "the variable, and b is the exponent (no '^'). None of the"
        print "functions in this program accept exponents greater than 3,"
        print "and all require that exponents > 1 be input. No coeffecients"
        print "or constants can be more than 99."
    elif function=="solver":
        print "This function is the main attraction, so to speak, of this algebra"
        print "machine. It asks for a statement and will either solve the equation"
        print "(cubic, quadratic, linear), or multiply/divide the groups. IMPORTANT:"
        print "it will only do the correct operation if a syntax is followed."
        print "Use '(x)(y)' for multiplication and '(x)/(y)' for division, where"
        print "x and y are polynomials no larger than a cubic. To solve an equation,"
        print "enter it without parentheses (the '=0' is not required.)"
    elif function=="factor":
        print "This function takes an equation, and checks if it factors"
        print "evenly, and if so, will print out the the equation in a"
        print "form similar to '(x+y)(x+z)', where y and z are constants."
    elif function=="absolute":
        print "This takes an absolute value equation/inequality of the"
        print "form '|x-y|=z', where x is the variable, y and z are constants,"
        print "and = is any of the operations =,<,>,<=,>=. It returns the"
        print "possible values/ranges of x in one or a pair of equation/"
        print "inequality statements."
    elif function=="lcm":
        print "Lowest Common Multiple. This takes from two to four numbers"
        print "separated by commas, and returns the LCM."
    elif function=="gcf":
        print "Greatest Common Factor. This takes from two to four numbers"
        print "separated by commas, and returns the GCF."
    elif function=="simplify":
        print "This function uses GCF and goes the extra step of factoring out"
        print "the GCF from two to four comma-separated list items. If you input"
        print "the first number as a numerator and the second as a denominator,"
        print "the output will be a reduced fraction."
    elif function=="sqrt":
        print "Finds the square root of a number. A negative number entered"
        print "will return with imaginary results."
    else:
        print "Incorrect entry. Possible choices are 'general', 'solver'"
        print "'factor', 'absolute', 'lcm', 'gcf', 'simplify', or 'sqrt'."
    reuse(0)


##BEGIN MATH FUNCTIONS


def reuse(curfunc):
    retry=" "
    print
    while retry!="y" and retry!="n":
        retry=raw_input("Reuse? (Y/N): ")
        retry=lowercase(retry)
    if retry=="n":
        return
    else:
        print
        if curfunc==0:
            help()
        elif curfunc==1:
            solver()
        elif curfunc==2:
            factor()
        elif curfunc==3:
            absolute()
        elif curfunc==4:
            lcm()
        elif curfunc==5:
            gcf()
        elif curfunc==6:
            simplify()
        elif curfunc==7:
            sqrt()

def numlist(num1=0, num2=0, num3=0, num4=0):
    nums=[num1,num2,num3,num4]
    if num1==0 or num2==0:
        numbers=raw_input("Enter a list of two to four numbers: ")
        numbers=removespaces(numbers)
        if numbers[len(numbers)-1] not in "1234567890":
            numbers=numbers[:len(numbers)-1]
        numbers+=","
    else:
        numbers=nums
    numcount=0
    count=0
    string=""
    while count<len(numbers):
        if numbers[count]==",":
            nums[numcount]=int(string)
            numcount+=1
            string=""
        else:
            string+=str(numbers[count])
        count+=1
    return nums

def lowercase(string):
    out=""
    for i in string:
        if ord(i)>64 and ord(i)<91:
            out+=chr(ord(i)+32)
        else:
            out+=i
    return out

def stringsetup(string):
    out=""
    for i in string:
        if i!=" ":
            out+=i
    string=out
    out=""
    for i in string:
        if (ord(i)>64 and ord(i)<91) or (ord(i)>96 and ord(i)<123):
            out+="x"
        else:
            out+=i
    string=out
    out=""
    for i in string:
        if i in "x1234567890()+-/=<>|":
            out+=i
    return out

def converttostring(listt):
    copylistt=copy.deepcopy(listt)
    count=0
    while count<len(copylistt):
        if int(copylistt[count])==copylistt[count]:
            copylistt[count]=int(copylistt[count])
        count+=1
    count=0
    while count<len(copylistt):
        if copylistt[count]>0:
            copylistt[count]="+"+str(copylistt[count])
        count+=1
    out=""
    count-=1
    while count>=0:
        if copylistt[count]!=0:
            out+=str(copylistt[count])+"x"+str(count)
        count-=1
    count=0
    while count<len(out):
        if out[count]=="x" and out[count+1]=="1":
            out=out[:count+1]+out[count+2:]
        elif out[count]=="x" and out[count+1]=="0":
            out=out[:count]
        count+=1
    count=0
    while count<len(out):
        if out[count]=="x" and out[count-1]=="1":
            out=out[:count-1]+out[count:]
        count+=1
    if out[0]=="+":
        out=out[1:]
    return out

def setupandcoeffs(eq=""):
    if eq=="":
        eq=raw_input("Enter statement: ")
    count=0
    while count<len(eq):
        if eq[count]=="=":
            eq=eq[:count]
            break
        count+=1
    eq=stringsetup(eq)
    eq=findcoeffs(eq)
    return eq

def findcoeffs(eq):
    if eq[len(eq)-2:]=="=0":
        eq=eq[:len(eq)-2]
    if eq[len(eq)-1:]=="=":
        eq=eq[:len(eq)-1]
    if eq[len(eq)-1]!="x" and eq[len(eq)-2]!="x":
        eq+="x0"
    else:
        eq+="+0x0"
    eq=stringsetup(eq)
    coeffs=[0]*4
    count=0
    negative=False
    singlenegative=False
    doublenegative=False
    temp=0
    while count<len(eq):
        if eq[count]=="x":
            if count>0 and eq[count-1]=="-":
                negative=True
            elif count>1 and eq[count-2]=="-":
                singlenegative=True
            elif count>2 and eq[count-3]=="-":
                doublenegative=True
            if count==0 or eq[count-1] in "+-=":
                if eq[count+1] not in "234":
                    temp+=1
                    if negative==True:
                        temp*=-1
                    coeffs[1]+=temp
                else:
                    temp+=1
                    if negative==True:
                        temp*=-1
                    coeffs[int(eq[count+1])]+=temp
            elif count==len(eq)-1 or eq[count+1] not in "234":
                if eq[count+1]=="0":
                    temp+=int(eq[count-1])
                    if singlenegative==True:
                        temp*=-1
                    if count>=2 and eq[count-2] not in "+-=":
                        temp+=int(eq[count-2])*10
                        if doublenegative==True:
                            temp*=-1
                    coeffs[0]+=temp
                else:
                    temp+=int(eq[count-1])
                    if singlenegative==True:
                        temp*=-1
                    if count>=2 and eq[count-2] not in "+-=":
                        temp+=int(eq[count-2])*10
                        if doublenegative==True:
                            temp*=-1
                    coeffs[1]+=temp
            else:
                temp+=int(eq[count-1])
                if singlenegative==True:
                    temp*=-1
                if count>=2 and eq[count-2] not in "+-=":
                    temp+=int(eq[count-2])*10
                    if doublenegative==True:
                        temp*=-1
                coeffs[int(eq[count+1])]+=temp
        negative=False
        singlenegative=False
        doublenegative=False
        temp=0
        count+=1
    return coeffs

def moveleft(eq, consttoright=False):
    eq=stringsetup(eq)
    count=0
    left=""
    right=""
    while count<len(eq) and eq[count]!="=":
        left+=eq[count]
        count+=1
    count+=1
    while count<len(eq):
        right+=eq[count]
        count+=1
    if left=="":
        left="0"
    if right=="":
        right="0"
    left=findcoeffs(left)
    right=findcoeffs(right)
    count=0
    while count<len(left):
        left[count]-=right[count]
        count+=1
    if consttoright and left[0]!=0:
        right=left[0]*-1
        left[0]=0
        left=converttostring(left)
        return left+"="+str(right)
    else:
        left=converttostring(left)
        return left+"=0"

def primefac(num):
    factors=[]
    count=2
    while count<=num:
        if not num%count:
            factors+=[count]
            num=num/count
            count=1
        count+=1
    return factors

def gcfmath(num1, num2):
    factors=[1]
    count=2
    while count<=min(num1, num2):
        if not num1%count and not num2%count:
            factors+=[count]
            num1/=count
            num2/=count
            count=1
        count+=1
    out=1
    for i in factors:
        out*=int(i)
    return out


def lcmmath(num1, num2):
    count=0
    num1=primefac(num1)
    num2=primefac(num2)
    while count<len(num1):
        if num1[count] in num2:
            del num1[count]
        count+=1
    factors=num1+num2
    out=1
    for i in factors:
        out*=int(i)
    return out

def simplifymath(num1, num2, num3=0, num4=0):
    out=[]
    gcf=gcfmath(num1, num2)
    if num3!=0:
        gcf=gcfmath(gcf, num3)
    if num4!=0:
        gcf=gcfmath(gcf, num4)
    num1/=gcf
    num2/=gcf
    out=[num1, num2]
    if num3!=0:
        num3/=gcf
        out+=[num3]
    if num4!=0:
        num4/=gcf
        out+=[num4]
    return out

def linearmath(coeffs):
    roots=[0]*3
    roots[1]=None
    roots[2]=None
    a=coeffs[1]
    b=coeffs[0]
    roots[0]=(-1*b)/a
    return roots

def quadmath(coeffs):
    roots=[0]*3
    roots[2]=None
    a=float(coeffs[2])
    b=float(coeffs[1])
    c=float(coeffs[0])
    d=((b**2)-(4*a*c))
    if d==0:
        roots[0]=(((-b)+round(math.sqrt(d),3))/(2*a))
        roots[1]=roots[0]
    elif d<0:
        roots[0]=None
        roots[1]=None
    else:
        roots[0]=(((-b)+round(math.sqrt(d),3))/(2*a))
        roots[1]=(((-b)-round(math.sqrt(d),3))/(2*a))
    return roots

def cubicmath(coeffs):
    roots=[0]*3
    a=float(coeffs[3])
    b=float(coeffs[2])
    c=float(coeffs[1])
    d=float(coeffs[0])
    x=((3*c/a)-((b**2)/(a**2)))/3
    y=((2*(b**3)/(a**3))-(9*b*c/(a**2))+(27*d/a))/27
    z=((y**2)/4)+((x**3)/27)
    if z>0:
        #roots[0]=(cuberoot((-1*(y/2))+math.sqrt(z)))+(cuberoot((-1*(y/2))-math.sqrt(z)))-(b/3*a)
        roots[1]=None
        roots[2]=None
    elif x==0 and y==0 and z==0:
        #roots[0]=-1*(cuberoot(d/a))
        roots[1]=roots[0]
        roots[2]=roots[0]
    else:
        i=math.sqrt(((y**2)/4)-z)
        #j=cuberoot(i)
    return roots

def multiplymath(eq):
    pairs=0
    string=""
    for i in eq:
        if i=="(":
            pairs+=1
    if pairs==1:
        return eq
    count=0
    for i in eq:
        if i==")":
            count+=1
        string+=str(i)
        if count==2:
            break
    eq=eq[len(string):]
    nums=[[],[]]
    count=-1
    curstr=""
    for i in string:
        if i=="(":
            count+=1
        curstr+=str(i)
        if i==")":
            nums[count]=curstr[1:len(curstr)-1]
            curstr=""
    nums[0]=findcoeffs(nums[0])
    nums[1]=findcoeffs(nums[1])
    out=[0]*(len(nums[0])*2)
    count=0
    scount=0
    while count<len(nums[0]):
        while scount<len(nums[1]):
            out[count+scount]+=(nums[0][count]*nums[1][scount])
            scount+=1
        scount=0
        count+=1
    out=converttostring(out)
    if pairs>2:
        eq+="("+out+")"
        multiply(eq)
    else:
        return out

def dividemath(eq):
    string=""
    count=0
    for i in eq:
        if i==")":
            count+=1
        string+=str(i)
        if count==2:
            break
    eq=eq[len(string):]
    nums=[[],[]]
    count=-1
    curstr=""
    for i in string:
        if i=="(":
            count+=1
        curstr+=str(i)
        if i==")":
            nums[count]=curstr[1:len(curstr)-1]
            curstr=""
    nums[0]=findcoeffs(nums[0])
    nums[1]=findcoeffs(nums[1])
    out=[0]*(len(nums[0])*2)
    count=0
    while count<2:
        if nums[count][3]==0 and nums[count][2]==0 and nums[count][1]!=0:
            nums[count]=linearmath(nums[count])
        elif nums[count][3]==0 and nums[count][2]!=0:
            nums[count]=quadmath(nums[count])
        #elif eq[3]!=0:
            #nums[count]=cubicmath(nums[count])
        count+=1
    count=0
    while count<len(nums[0]):
        if nums[0][count]!=None:
            nums[0][count]*=(-1)
        count+=1
    count=0
    while count<len(nums[1]):
        if nums[1][count]!=None:
            nums[1][count]*=(-1)
        count+=1
    count=0
    while count<3:
        scount=0
        while scount<3:
            if nums[0][count]==nums[1][scount]:
                nums[0][count]=None
            scount+=1
        count+=1
    count=0
    while count<len(nums[0]):
        if nums[0][count]!=None:
            nums[0][count]="("+converttostring([nums[0][count],1])+")"
        count+=1
    out=""
    for i in nums[0]:
        if i!=None:
            out+=str(i)
    if out=="":
        out="Not evenly divisble"
    else:
        out=multiplymath(out)
    return out

def polymath(eq):
    div=False
    count=0
    numerator=""
    denominator=""
    while count<len(eq):
        if eq[count]!="/":
            numerator+=eq[count]
        else:
            div=True
            break
        count+=1
    if div:
        count+=1
        while count<len(eq):
            denominator+=eq[count]
            count+=1
        print "Divided:",dividemath(numerator+denominator)
    else:
        print "Multiplied:",multiplymath(numerator)

def equation(eq):
    count=0
    eq=moveleft(eq)
    eq=findcoeffs(eq)
    if eq[3]==0 and eq[2]==0 and eq[1]!=0:
        eq=linearmath(eq)
        print "Solution:",eq[0]
    elif eq[3]==0 and eq[2]!=0:
        eq=quadmath(eq)
        if eq[0]==None and eq[1]==None:
            print "No solution."
        elif eq[0]==eq[1]:
            if int(eq[0])==eq[0]:
                eq[0]=int(eq[0])
            print "Double root:",eq[0]
        else:
            if int(eq[0])==eq[0]:
                eq[0]=int(eq[0])
            if int(eq[1])==eq[1]:
                eq[1]=int(eq[1])
            print "Two real roots:",eq[0],eq[1]
    elif eq[3]!=0:
        eq=cubicmath(eq)
        #different outputs for different combos of answers
    else:
        print "Invalid entry."


##BEGIN INTERFACE FUNCTIONS


def solver(eq=""):
    if eq=="":
        eq=raw_input("Enter statement: ")
    eq=stringsetup(eq)
    doPolymath=False
    for i in eq:
        if i in "()":
            doPolymath=True
    if doPolymath:
        eq=polymath(eq)
    else:
        eq=moveleft(eq)
        eq=equation(eq)
    reuse(1)

def factor(eq=""):
    eq=setupandcoeffs(eq)
    a=float(eq[2])
    b=float(eq[1])
    c=float(eq[0])
    d=((b**2)-(4*a*c))
    x=(((-b)+round(math.sqrt(d),3))/(2*a))
    y=(((-b)-round(math.sqrt(d),3))/(2*a))
    if x==int(x) and y==x:
        x*=-1
        x=int(x)
        if x>0:
            x="+"+str(x)
        x=str(x)
        print "(x"+x+")(x"+x+")"
    elif x==int(x) and y==int(y):
        x*=-1
        y*=-1
        x=int(x)
        y=int(y)
        if x>0:
            x="+"+str(x)
        if y>0:
            y="+"+str(y)
        x=str(x)
        y=str(y)
        print "(x"+x+")(x"+y+")"
    else:
        print "Non-factorable."
    reuse(2)

def newfactor(eq=""):
    eq=setupandcoeffs(eq)
    eq=cubicmath(eq)
    x=0
    y=0
    z=0
    out=""
    success=False
    if x==int(x) and y==int(y):
        x=int(x)
        y=int(y)
        if x>0:
            x="+"+str(x)
        if y>0:
            y="+"+str(y)
        out="(x"+x+")(x"+y+")"
        success=True
    else:
        out="Non-factorable."
    if success and z==int(z):
        z=int(z)
        if z>0:
            z="+"+str(z)
        out+="(x"+z+")"
    else:
        out="Non-factorable."

    print out
    reuse(2)

def absolute(eq=""):
    if eq=="":
        eq=raw_input("Enter equation, with |'s: ")
    eq=stringsetup(eq)
    left=""
    coeff=""
    leftoperation=""
    leftnumber=""
    operation=""
    right=""
    temp=0
    count=0
    while eq[count] not in "<>=":
        left+=eq[count]
        count+=1
    left=left[1:]
    left=left[:len(left)-1]
    if left[0]!="x":
        coeff=left[0]
        left=left[1:]
        if left[0]!="x":
            coeff+=left[1]
            left=left[1:]
    for i in left:
        if i in "+-":
            leftoperation=i
    for i in left:
        if i in "1234567890":
            leftnumber+=i
    if leftoperation=="+":
        leftnumber="-"+leftnumber
    while eq[count] not in "1234567890":
        operation+=eq[count]
        count+=1
    while count<len(eq):
        right+=eq[count]
        count+=1
    leftnumber=float(leftnumber)
    right=float(right)
    positive=abs(right)+leftnumber
    negative=(-1*abs(right))+leftnumber
    if coeff!="":
        coeff=float(coeff)
        positive/=coeff
        negative/=coeff
        if int(positive)==positive:
            positive=int(positive)
        if int(negative)==negative:
            negative=int(negative)
    if operation=="=":
        print "x="+str(positive)+" or x="+str(negative)
    elif operation=="<" or operation=="<=":
        print str(min(positive, negative))+operation+"x"+operation+str(max(positive, negative))
    elif operation==">":
        print "x<"+str(min(positive, negative))+" or x>"+str(max(positive, negative))
    else:
        print "x<="+str(min(positive, negative))+" or x>="+str(max(positive, negative))
    reuse(3)

def lcm(num1=0, num2=0, num3=0, num4=0):
    nums=numlist(num1, num2, num3, num4)
    out=lcmmath(nums[0], nums[1])
    if nums[2]!=0:
        out=lcmmath(out, nums[2])
    if nums[3]!=0:
        out=lcmmath(out, nums[3])
    print "LCM:",out
    reuse(4)
        
def gcf(num1=0, num2=0, num3=0, num4=0):
    nums=numlist(num1, num2, num3, num4)
    out=gcfmath(nums[0], nums[1])
    if nums[2]!=0:
        out=gcfmath(out, nums[2])
    if nums[3]!=0:
        out=gcfmath(out, nums[3])
    print "GCF:",out
    reuse(5)

def simplify(num1=0, num2=0, num3=0, num4=0):
    print num1, num2,
    if num3!=0:
        print num3,
    if num4!=0:
        print num4
    reuse(6)

def sqrt(num=0):
    i=False
    if num==0:
        num=input("Enter number: ")
    if num<0:
        num=abs(num)
        i=True
    num=round(math.sqrt(num), 3)
    if int(num)==num:
        num=int(num)
    if i==True:
        num=str(num)+"i"
    print "Square root:",num
    reuse(7)
