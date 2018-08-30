#Scientific Notation Converter

def expressionConvert(number, exponent):
    exponent=10**exponent
    return str(number*exponent)

def decimalConvert(number):
    exponent=0
    while number>=10 or number<1:
        number/=10
        exponent+=1
    return str(number) + " * 10^" + str(exponent)
    
print "Format: [decimal] * [10^x] OR [decimal]."
on=True
while on==True:
    number=raw_input("Enter number/expression: ")
    count=0
    decimal=""
    exponent=""
    expression=False
    while count<len(number):
        decimal=decimal+number[count]
        if number[count]==" ":
            expression=True
            count+=6
            exponent=number[count:]
            exponent=int(exponent)
        count+=1
    decimal=float(decimal)
    if expression==False:
        out=decimalConvert(decimal)
    else:
        out=expressionConvert(decimal, exponent)
    print out
    print
