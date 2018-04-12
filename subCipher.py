import os, sys
import string
import operator
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np

# This method will be used to get the frequencies of letters based on specific regex.
def getFreqs(cipher, regex):
    tempDict = {}
    # The regex to find two letter pairs.
    pattern = re.compile(regex)
    # Find all of the matches and return a iterator.
    matches = pattern.finditer(cipher)
    
    for match in matches:
        # Get the specific value from the iterator.
        pair = match.group()

        # If the cipher pair does exist then add a one to it in the dictionary.
        if (pair in tempDict.keys()):
            tempDict[pair] =  tempDict[pair] + 1

        # else this is the first time adding it into the dictionary
        else: 
            tempDict[pair] = 1
    
    return tempDict

# Get letter corresponding cipher text
def pairCipherLetters(freqDict, letterList):
    tempDict = {}

    for letter in letterList:
        maxLetter = max(freqDict.items(), key = operator.itemgetter(1))[0]
        del freqDict[maxLetter]
        tempDict[letter] = maxLetter
    
    return tempDict

# This method will decipher the cipher passed in.
def decipher(cipher, cipherPairs):
    for key, value in cipherPairs.items():
        cipher = cipher.replace(value, key)
    return cipher

def main():
    # I changed the order of these to help decipher. I first tried these common letters and made sure they were correct.
    commonLetters = ['e', 't', 'a', 's', 'r', 'i']
    
    # This dictionary will hold letter frequencies.
    letterFreqDict = {}

    cipher = None
    cipherLetterPairs = None
    
    # loads the cipher text from the file.
    with open(sys.path[0] + '\data\substitutionCipher.txt', 'r') as myfile:
        cipher = myfile.read().replace('\n', '')
    
    letterFreqDict = getFreqs(cipher, "[A-Z]")
    
    # I then acquired the 2 letter frequency of cipher pairs which started with G.
    twoLetterFreqDict = getFreqs(cipher, "G\w")

    # Pairs up each of the common letters with there cipher text equivalent.
    cipherLetterPairs = pairCipherLetters(letterFreqDict, commonLetters)
    
    # Here I will update dictionary with trial and error to try and form words.
    # First I tried the most commom letters.
    cipherLetterPairs['h'] = 'A'
    cipherLetterPairs['n'] = "R"
    cipherLetterPairs['d'] = 'O'
    cipherLetterPairs['o'] = 'I'
    cipherLetterPairs['u'] = 'E'
    
    # From here it was trial and error until I got the first couple of words and realized what where the saying was from.
    cipherLetterPairs['l'] = 'X'
    cipherLetterPairs['p'] = 'W'
    cipherLetterPairs['f'] = 'H'
    cipherLetterPairs['c'] = 'P'
    cipherLetterPairs['v'] = 'Q'
    cipherLetterPairs['m'] = 'V'
    cipherLetterPairs['w'] = 'T'
    cipherLetterPairs['k'] = 'U'
    cipherLetterPairs['g'] = 'M'
    cipherLetterPairs['b'] = 'Z'
    cipherLetterPairs['y'] = 'L'
    cipherLetterPairs['x'] = 'J'
    
    print("Original cipher: \n" + cipher)

    decipheredText = decipher(cipher, cipherLetterPairs)
    print("After applying common letters: " + decipheredText)
    

if __name__ == '__main__':
    main()