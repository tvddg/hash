def RightRotate(x, shift):
    rotated = ((x >> shift) | (x << (32 - shift))) & 0xFFFFFFFF
    return rotated

def MedsigZero(x):
    return RightRotate(x, 7) ^ RightRotate(x, 18) ^ (x >> 3) 
def MedsigOne(x):
    return RightRotate(x, 17) ^ RightRotate(x, 19) ^ (x >> 10)

def calculateNextWord(w0, w1, w9, w14):
    w0 = int(w0, 2)
    w1 = int(w1, 2)
    w9 = int(w9, 2)
    w14 = int(w14, 2)

    nextWord = (w0 + MedsigZero(w1) + w9 + MedsigOne(w14)) & 0xFFFFFFFF
    return format(nextWord, "032b")

def isPrime(num):
        for k in range(2, int(num**(1/2)) + 1):
            if num % k == 0:
                return False
        return True

def get_mantissa_bits(val, nbits=32):
    frac_part = val - int(val)
    bits = ''
    for _ in range(nbits):
        frac_part *= 2
        if frac_part >= 1:
            bits += '1'
            frac_part -= 1
        else:
            bits += '0'
    return bits

def initHashValues():
    hash_value = []
    for num in range(2, 20):
        if isPrime(num):
            hash_value.append(get_mantissa_bits(num**(1/2)))
    return hash_value

def initKconsts():
    k_consts = []
    for num in range(2, 312):
        if isPrime(num):
            k_consts.append(get_mantissa_bits(num**(1/3))) 
    return k_consts

def variablesToInt(variables):
    result = []
    for var in variables:
        result.append(int(var, 2))
    return result

def variablesToBin(variables):
    result = []
    for var in variables:
        result.append(format(var, "032b"))
    return result

def updateVariables(variables, curr_k, curr_w):
    (a, b, c, d, e, f, g, h) = variablesToInt(variables)
    k = int(curr_k, 2)
    w = int(curr_w, 2)
    capsig1 = CapsigOne(e)
    choice = Choice(e, f, g)
    temp1 = Temp1(h, capsig1, choice, k, w)

    capsig0 = CapsigZero(a)
    majority = Majority(a, b, c)
    temp2 = Temp2(capsig0, majority)

    new_variables = [ ((temp1 + temp2) & 0xFFFFFFFF), a, b, c, 
            ((d + temp1) & 0xFFFFFFFF), e, f, g ]
    return variablesToBin(new_variables)

def CapsigZero(x):
    return (RightRotate(x, 2) ^ RightRotate(x, 13) ^ RightRotate(x, 22)) & 0xFFFFFFFF
def CapsigOne(x):
    return (RightRotate(x, 6) ^ RightRotate(x, 11) ^ RightRotate(x, 25)) & 0xFFFFFFFF

def Choice(e, f, g):
    return ((e & f) ^ ((~e) & g)) & 0xFFFFFFFF
def Majority(a, b, c):
    return ((a & b) ^ (a & c) ^ (b & c)) & 0xFFFFFFFF

def Temp1(h, capsig1, choice, k, w):
    return (h + capsig1 + choice + k + w) & 0xFFFFFFFF
def Temp2(capsig0, majority):
    return (capsig0 + majority) & 0xFFFFFFFF