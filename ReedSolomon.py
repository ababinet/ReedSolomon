import sys
"""
ReedSolomon.py
Alia Babinet, Adela Dujsikova, and Lita Theng
Final project for CS252: Algorithms at Carleton College

Input: <fileName> <errorSize>
<fileName> -> text file containing bit values in EITHER hexadecimal or binary
(NOTE: The program will not execute properly if the message is not hexadecimal or binary)
<errorSize> -> the number of error symbols (amount of error correction)

Output: the message along with the error correction bits. Following this there is then
a corruption check (should come back false). An error is then introduced and the corruption check is run again
"""

## Global variables to be used in the computation##
# -- exponents (anti-logarithms)
GFEXP = [0] * 512
# -- logarithms
GFLOG = [0] * 256

## Processes the inputted file and extracts the message
def readFile(fileName):
    inputFile = open(fileName, "r")
    bitStream = []
    Lines = inputFile.readlines()
    for line in Lines:
        line = line.rstrip("/n")
        # accounting for hexidecimal messages
        if 'x' in line:
            bitStream.append(int(line,16))
        # accounting for binary messages
        else:
            bitStream.append(int(line, 2))
    inputFile.close
    return bitStream

## Initializes the exponential and logarithmic tables that are used in
## multiplication and division (this makes the algorithm faster as
## it removes the need to re-calacuate values)
def initialize():
    ### Galois fields math - the inputs are binary
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

## Define multiplication and division functions
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
        return GFEXP[((GFLOG[x]-GFLOG[y])+255) % 255]

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

## generates irreducible generator polynomial
def generatorPoly(errorSize):
    
    val = [1]
    for i in range(0, errorSize):
        val = polyMul(val, [1, GFEXP[i]])
    return val

## main encoding function that divides the message by the generator polynomial
def RSEncode(input, errorSize):
    gen = generatorPoly(errorSize)
    modInput = input + [0] * (len(gen)-1)

    res, remainder = polyDiv(modInput, gen)

    return input + remainder

## Partial decoding
## This section is at the point where the a check of corruption is done
## no error-correction has been implemented

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

if __name__ == '__main__':
    initialize()
    fileName = sys.argv[1]
    errorSize = int(sys.argv[2])

    bitStream = readFile(fileName)
    print(type(bitStream[0]))
    encodedMessage = RSEncode(bitStream, errorSize)
    printEncoded = []

    for i in range(len(encodedMessage)):
        printEncoded.append(bin(encodedMessage[i]))
    print("This is the encoded message for error size: " + str(errorSize) + ": " + str(printEncoded))

    #message not corrupted yet, want to show that isCorrupted works
    print("Before corruption...")
    if isCorrupted(encodedMessage, errorSize):
        print("This message has been corrupted: " + str(printEncoded))
    else:
        print("This message has not been corrupted: " + str(printEncoded))

    #corrupting message
    encodedMessage[1] = 24

    #checking if message is corrupted, should return that it is.
    print("After corruption...")
    if isCorrupted(encodedMessage, errorSize):
        print("This message has been corrupted: " + str(printEncoded))
    else:
        print("This message has not been corrupted: " + str(printEncoded))
    
