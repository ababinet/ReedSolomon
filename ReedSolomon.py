import sys
"""
ReedSolomon.py
Alia Babinet, Adela Dujsikova, and Lita Theng
Final project for CS252: Algorithms at Carleton College

Input: <fileName> <errorSize>
<fileName> -> text file containing bit values in either hexadecimal or binary
<errorSize> -> the number of error symbols (amount of error correction)
"""
def readFile(fileName):
	inputFile = open(fileName, "r")
	bitStream = []
	Lines = inputFile.readlines()
	for line in Lines:
		line = line.replace('\n','')
		if line[1] == "x":
			bitStream.append(hex(int(line,16)))
		else:
			bitStream.append
	inputFile.close
	return bitStream

### Galois fields math - the inputs are binary

# -- exponents (anti-logarithms)
GFEXP = [0] * 512
# -- logarithms
GFLOG = [0] * 256
	
# Define the exponential and logarithmic tables
GFEXP[0] = 1
val = 1
for i in range(1, 255):
	val <<= 1 # bitwise right shift and value assignment
	if (val & 256): # & performs bitwise operations
		val ^= 285
			
	# update the tables
	GFEXP[i] = val
	GFLOG[val] = i
		
# finalize the exponential table
for i in range(255, 512):
	GFEXP[i] = GFEXP[i - 255]

# Define basic operations in Galois fields

def gf_add(x, y):
    return x ^ y

def gf_sub(x, y):
    return x ^ y

# NOTE: since we are in mod 2, addition and subtraction gives the same result
    
def gf_mul(x, y):
    if x == 0 or y == 0:
        return 0
    else:
        return GFEXP[(GFLOG[x] + GFLOG[y]) % 255]

def gf_div(x, y):
    if y == 0:
        sys.exit("Division by 0")
    if x == 0:
        return 0
    else:
        return GFEXP[(GFLOG[x]-GFLOG[y]+255) % 255]

def gf_pow(x, power):
    return GFEXP[(GFLOG[x] * power) % 255]

def polyMul(A, B):
    # initialize the product
    size = len(A) + len(B) - 1
    product = [0] * size
	
    # multiply
    for i in range(0, len(B)):
        for j in range(0, len(A)):
            p = gf_mul(A[j], B[i])
            product[i+j] = gf_add(product[i+j], p)
    # return the product result
    return (product)

def polyDiv(dividend, divisor):
    # initialize
    output = list(dividend)
    length = len(dividend) - (len(divisor)-1)

    # divide
    for i in range(0, length):
        if output[i]: # log(0) is undefined
            for j in range(1, len(divisor)):
                if divisor[j]: # log(0) is undefined
                    output[i + j] ^= gf_mul(divisor[j], output[i])
    # separate the result of division and the remainder
    separator = -(len(divisor)-1)
    return output[:separator], output[separator:]

def generatorPoly(errorSize):
    '''generates irreducible generator polynomial'''
    val = [1]
    for i in range(0, errorSize):
        val = polyMul(val, [1, GFEXP[i]])
    return val

def RSEncode(input, errorSize):
    '''main encoding function that divides the message by the generator polynomial'''
    gen = generatorPoly(errorSize)
    modInput = input + [0] * (len(gen)-1)

    res, remainder = polyDiv(modInput, gen)
    
    return input + remainder


# testing code for encoding
msg_hex = [0x40, 0xd2, 0x75, 0x47, 0x76, 0x17, 0x32, 0x06, 0x27, 0x26, 0x96, 0xc6, 0xc6, 0x96, 0x70, 0xec]

msg_bin = [0b01000000, 0b11010010, 0b01110101, 0b01000111, 0b01110110, 0b00010111, 0b00110010, 0b0110, 0b00100111, 0b00100110, 0b10010110, 0b11000110, 0b11000110, 0b10010110, 0b01110000, 0b11101100]

msg = RSEncode(msg_bin, 10)

for i in range(0,len(msg)):
    print(hex(msg[i]), end=' ')
    #print(bin(msg[i]), end=' ')


# Partial decoding

def gf_poly_eval(poly, x):
    '''evaluates a polynomial at a particular value of x'''
    eval = poly[0]
    for i in range(1, len(poly)):
        eval = gf_add(gf_mul(eval, x), poly[i])
    return eval

def isCorrupted(message, errorSize):
    '''reports whether a message has been corrupted'''
    syndromes = [0] * errorSize
    for i in range(0, errorSize):
        syndromes[i] = gf_poly_eval(message, GFEXP[i])
    return max(syndromes) != 0

msg[0] = 0xd2
print(isCorrupted(msg,10))

if __name__ == '__main__':
	fileName = sys.argv[0]
	errorSize = sys.argv[1]
	
	bitStream = readFile(fileName)
	
	encodedMessage = RSncode(bitStream, errorSize)
	print("This is the encoded message for error size: " + errorSize + ": " + encodedMessage
	
	if isCorrupted(encodedMessage, errorSize):
		print("This message has been corrupted: " + encodedMessage)
	else:
		print("This message has not been corrupted: " + encodedMessage)
