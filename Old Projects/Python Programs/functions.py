#assorted functions

def factors(num):
    """Int > 0 -> Factor list"""
    out=[]
    for i in range(1, num+1):
        if not num%i:
            out+=[i]
    return out

def numFactors(num):
    """Int > 0 -> Number of factors"""
    return len(factors(num))

def isPrime(num):
    return len(factors(num))<=2

def primeFac(num):
    """Int > 0 -> Prime factorization"""
    factors=[]
    count=2
    while count<=num:
        if not num%count:
            factors+=[count]
            num=num/count
            count=1
        count+=1
    return factors

def reverseString(string):
    n=0
    temp=""
    while n<len(string):
        temp=temp+string[(len(string)-(n+1))]
        n+=1
    return temp

def uppercase(string):
    out=""
    for i in string:
        if ord(i)>96 and ord(i)<123:
            out+=chr(ord(i)-32)
        else:
            out+=i
    return out

def lowercase(string):
    out=""
    for i in string:
        if ord(i)>64 and ord(i)<91:
            out+=chr(ord(i)+32)
        else:
            out+=i
    return out

def avg(seq):
    """Number list -> Average value"""
    temp=0
    for i in seq:
        temp+=i
    return temp/float(len(seq))
