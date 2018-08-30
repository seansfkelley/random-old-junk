#cypher with key

from random import randint
alphabet="abcdefghijklmnopqrstuvwxyz"

def encode(string, shift):
    if shift<1 or shift>25:
        return "Illegal shift value."
    string=lowercase(string)
    code=shifter(string, shift, 1)
    print "Encoded: " + code
    print "Key: " + keycode(shift)

def decode(string, shift):
    shift=lowercase(shift)
    shift=convert(shift)
    code=shifter(string, shift, 0)
    print "Decoded: " + code

def shifter(string, shift, caller):
    output=""
    count=0
    while count<len(string):
        if ord(string[count])>96 and ord(string[count])<123:
            if caller==1:
                temp=97-shift
            else:
                temp=97+shift
            temp=ord(string[count])-temp
            while temp>25:
                temp-=26
            output+=alphabet[temp]
        elif string[count]==" ":
            output+=" "
        count+=1
    return output

def convert(string):
    count=0
    shift=0
    while count<len(string):
        shift+=ord(string[count])
        count+=1
    return (shift/3)-96

def keycode(shift):
    shift=(shift+96)*3
    if shift<291 or shift>366:
        return "Invalid value."
    else:
        valid=False
        while valid==False:
            count=0
            rand=0
            key=""
            temp=shift
            while count==0 or count==1:
                rand=randint(97, 122)
                key+=chr(rand)
                temp-=rand
                count+=1
            key+=chr(temp)
            valid=True
            if ord(key[2])<97 or ord(key[2])>122:
                valid=False
        return key

def lowercase(string):
    out=""
    count=0
    while count<len(string):
        if ord(string[count])>64 and ord(string[count])<91:
            out+=chr(ord(string[count])+32)
        else:
            out+=string[count]
        count+=1
    return out

print 'Commands: encode("message to encode", int distance to shift letter)'
print '          decode("encoded message", "code given by encoder")'
print 'When you encode something, a key code is given so the decoder knows'
print 'what distance to shift the units back (during decoding) so it is readable.'
print 'Legal shift values: 0<value<26'
