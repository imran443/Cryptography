import os, sys
import string
import operator
import re
import copy
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from functools import reduce

# Utlity method to get the factors of a prime number.
def prime_factors(n):
    i = 2
    factors = []
    while (i * i <= n):
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

# Used to compute b^-1 mod a
def multiplicativeInverse(a, b):
    a0 = a
    b0 = b
    t0 = 0
    t = 1
    q = math.floor(a0/b0)
    r = a0 - (q * b0)

    while(r > 0):
        temp = (t0 - (q * t)) % a
        t0 = t
        t = temp
        a0 = b0
        b0 = r
        q = math.floor(a0/b0)
        r = a0 - (q * b0)
    
    if (b0 != 1):
        print(b + ' has no inverse mod ' + a)
    else:
        return t

# The main part of the program. Deciphers the RSA encryption by being fed in a list of cipher numbers.
# As well as a which is the private key number and n. 
def decipher(cipherList, a, n):
    decryptedMsg = []

    for cipherNum in cipherList:
        # Dycrypts the RSA encryption.
        decryptedNum = modExponentation(cipherNum, a, n)

        i = 0
        
        # Finds c3 in the decrypted number.
        while((decryptedNum - i) % 26 != 0):
            i += 1
        
        # These are the 3 letters aftering breaking the encoding.
        c1 = None
        c2 = None
        c3 = None
              
        c1 = int(decryptedNum / (26*26))
        c2 = int((decryptedNum - 26*26*c1) / 26)
        c3 = int(decryptedNum - 26*26*c1 - 26*c2)
        
        # Convert to letters.
        c1 = chr(c1 + 65)
        c2 = chr(c2 + 65)          
        c3 = chr(c3 + 65)

        # Add to the a list for later.
        decryptedMsg.append(c1)
        decryptedMsg.append(c2)
        decryptedMsg.append(c3)

    return decryptedMsg


# Special method to calculate the private key.
def modExponentation(x,e,m):
    X = x
    E = e
    Y = 1
    while E > 0:
        if E % 2 == 0:
            X = (X * X) % m
            E = E/2
        else:
            Y = (X * Y) % m
            E = E - 1
    return Y

# Returns all of the factors of a number.
def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(pow(n, 0.5) + 1)) if n % i == 0)))

def main():
    cipher = np.genfromtxt(sys.path[0] + r'\data\RSACipher.txt', dtype='int')
    decipheredList = None
    decipheredMsg = None
    # Set all of the initial values for the RSA decryption
    n = 18209
    primeFactors = prime_factors(n)
    p = primeFactors[0]
    q = primeFactors[1]
    phi = (p-1)*(q-1)
    b = 3001
    a = multiplicativeInverse(phi, b)
    
    #Gets the deciphered text 
    decipheredList = decipher(cipher, a, n)
    decipheredMsg = ''.join(decipheredList)
    print("Deciphered Text:", decipheredMsg)



if __name__ == '__main__':
    main()