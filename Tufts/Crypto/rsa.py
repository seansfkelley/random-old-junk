import sys
import time
import math
import subprocess
import struct

# A ~2048-bit prime.
p = 4667104771352721798051879278582055573480191264773582700016346261853876528815815940222390955079656853994138856871882286357445046816243315665908328410852711372589350653595310800429040345883513641387349768146392780230946660360435488033524364239682948371872228954881350889635153697454768058256564966258497827329674123694735557853911833773911447484988194073704725646821558508244530409528044157873087570151808476050730921048682284721385548692379636690989493912753915248998160262161050705473834341846165285780447398627211568915545809661899091324133442556467830237263419762713332770516444265693912887778478244886823816147581
q = 2 * p + 1

PRG_EXECUTABLE = './bbs'
SEED_SIZE = 128

class Struct:
    pass


def get_random_int(n_bits):
    rand = subprocess.Popen('%s %d %d' % (PRG_EXECUTABLE, SEED_SIZE, n_bits), stdout = subprocess.PIPE)
    return int(rand.communicate()[0])


def exp(b, e, n):
    powers = [(1, b)]
    cur_exp = 2
    while cur_exp <= e:
        b = (b ** 2) % n
        powers.append((cur_exp, b))
        cur_exp *= 2
    
    cur_exp /= 2
    
    powers.reverse()
    for (exp, power) in powers:
        if cur_exp + exp <= e:
            b = (b * power) % n
            cur_exp += exp
    
    return b 

def gcd(a, b):
    if (a > b):
        large, small = a, b
    else:
        large, small = b, a
    
    while small != 0:
        temp = small
        small = large % small
        large = temp
    
    return large

def inverse(x, p):
    quotients = []
    large, small = p, x % p
    
    while small != 0:
        temp = small
        small = large % small
        quotients.append(large/temp)
        large = temp
    
    prev, cur = 0, 1
    for q in quotients[:-1]:
        temp = cur
        cur = prev - q*cur
        prev = temp
    
    return cur % p


def generate(p, q):
    totient = (p-1) * (q-1)
    
    pk = Struct()
    sk = Struct()
    
    pk.e = totient
    while gcd(pk.e, totient) != 1:
        pk.e = get_random_int(2, totient - 1)
    
    sk.d = inverse(pk.e, totient)
    assert pk.e * sk.d % totient == 1
    
    pk.n = sk.n = p * q
    pk.n_bits = math.floor(math.log(pk.n, 2))
    
    return (pk, sk)

def encrypt(m, pk):
    return exp(m, pk.e, pk.n)

def decrypt(c, sk):
    return exp(c, sk.d, sk.n)


def pad_message(m, pk):
    pad_size = math.floor(pk.n_bits/8 - len(m)) # In 8-bit characters.
    if (pad_size < 0):
        return pad_message(m[:len(m)/2], pk) + pad_message(m[len(m)/2:], pk)
    
    m = struct.pack('c', chr(0)) + m
    pad_size -= 1
    while (pad_size > 0):
        m = struct.pack('c', chr(get_random_int(0, 255))) + m
        pad_size -= 1
    
    return [m]

def unpad_message(m_list):
    reverse = m[::-1]
    unpadded = ''
    for c in reverse:
        if ord(c) == 0:
            break
        else:
            unpadded += c
    return unpadded[::-1]


def string_to_number(s):
    reverse = s[::-1]
    current_power = 1
    number = 0
    for c in reverse:
        number += current_power * ord(c)
        current_power <<= 8
    return number

def number_to_string(n):
    m = ''
    while n > 0:
        m = chr(n % 256) + m
        n >>= 8
    return m


print get_random_int(512)

# PK, SK = generate(p, q)
# 
# m = raw_input()
# 
# pad_list = pad_message(m, PK)
# c_list = []
# for p in pad_list:
#     c_list.append(string_to_number(p))
# 
# start = time.time()
# for c in c_list:
#     temp = number_to_string(c)
#     assert c == decrypt(encrypt(c, PK), SK)
# 
# dec_m = ''
# for c in c_list:
#     dec_m += unpad_message(number_to_string(c))
# print dec_m