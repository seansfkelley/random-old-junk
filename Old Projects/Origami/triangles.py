from operator import indexOf

def main():
    line=raw_input('enter 6 comma-separated numbers or "q" to quit: ')
    while line not in 'Qq':
        line=line.split(',')
        for i in range(6):
            line[i]=float(line[i])
        if illegal(line[:3]) or illegal(line[3:]):
            print 'NOT VALID'
        else:
            check(line[:3],line[3:])
        line=raw_input('enter 6 comma-separated numbers or "q" to quit: ')

def illegal(triangle):
    if triangle[0]>=triangle[1]+triangle[2] or\
       triangle[1]>=triangle[0]+triangle[2] or\
       triangle[2]>=triangle[0]+triangle[1]:
        return True
    return False

def check(tri1, tri2):
    values,letters=specialsort(tri1,tri2)
    results=[]
    for i in range(3):
        results+=[tri1[i]/values[i]]
    if results[0]==results[1]==results[2]:
        if letters[0][1] not in letters[1]:
            letters[0]=letters[0][1]+letters[0][0]
        if letters[1][1] not in letters[2]:
            letters[1]=letters[1][1]+letters[1][0]
        print letters[0]+letters[1][1]
    else:
        print 'NONE'

def specialsort(ref, tosort):
    ref, tosort=list(ref),list(tosort)
    results=[None]*3
    letters, refletters=['a']*3,['DE','EF','FD']
    temp=indexOf(ref,max(ref))
    results[temp]=max(tosort)
    letters[temp]=refletters[indexOf(tosort,max(tosort))]
    temp=indexOf(ref,min(ref))
    results[temp]=min(tosort)
    letters[temp]=refletters[indexOf(tosort,min(tosort))]
    for i in results:
        if i in tosort:
            tosort.remove(i)
    for i in letters:
        if i in refletters:
            refletters.remove(i)
    results[indexOf(results,None)]=tosort[0]
    letters[indexOf(letters,'a')]=refletters[0]
    return[results,letters]

if __name__=='__main__':
    main()
