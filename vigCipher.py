import os, sys
import string
import operator
import re
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from functools import reduce

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

def getFactors(cipher, dups):
    factorDict = {}
    for dup in dups:
        for key, item in dup.items():
            # The regex to find two letter pairs.
            pattern = re.compile(key)
            # Find all of the matches and return a iterator.
            matches = pattern.finditer(cipher)
            a = matches.__next__().start()
            b = matches.__next__().start()
            factorSet = factors(b-a)
            for factor in factorSet: 
                # If the factor does exist then add a one to it in the dictionary.
                if (factor in factorDict.keys()):
                    factorDict[factor] =  factorDict[factor] + 1

                # else this is the first time adding it into the dictionary
                else: 
                    factorDict[factor] = 1
    
    return factorDict

# Size of the duplicates are passed in. So for example find duplicates of size 3 in the cipher text.
def getAllDups(cipher, size):
    cipherList = list(cipher)
    cipherArray = np.array(cipherList, dtype='str')
    
    # This list will hold all of the reoccuring dups. Each cell will have dictionary of dups.
    dupsList = []

    # The index for splicing the array.
    k = size
    for i in range(cipherArray.shape[0]):
        
        # k can't be larger than the list.
        if (k <= cipherArray.shape[0]):
           
            # Get the spliced array and convert it into a list.
            tempList = np.ndarray.tolist(cipherArray[i:k])
            
            # Change that list into a string and use it to search.
            regex = ''.join(tempList)
            
            # Get the frequncy for this specific regex. This returns a dictionary (hash map)
            freqDict = getFreqs(cipher, regex)
            
            # Makes sure that no duplicate dictionaries are added to the list.
            if (any(regex in d for d in dupsList) == False and freqDict[regex] > 1):
                dupsList.append(freqDict)
            
            k += 1
    
    
    return dupsList

# This method creates the specific groups for each part of the cipher key. From position 1 to 5 in each case.
def createGroups(cipher, keyLength):
    groupDict = {}
    groupList = []

    for i in range(keyLength):
        index = i
        for j in range(len(cipher)):
            if (j > 0):
                # This index is updated to based on the cipher key length. 
                # So for example it will start from position 1 and move 5 spots over each time. 
                # Then when the index is incremented it will start from position 2 and move 5 spots etc.
                index += keyLength
                if (index < len(cipher)):
                    groupList.append(cipher[index])
            else:
                groupList.append(cipher[i])
        
        # Store and empty the list after.
        groupDict[i+1] = copy.deepcopy(groupList)
        groupList = []
    
    return groupDict

def getGroupPrecents(cipher, groupsDict):
    # Will be used to aggregate the frequencies of each letter in the cipher text.
    alphabetDict = dict.fromkeys(string.ascii_uppercase, 0)
    groupFreqsList = []

    for letterList in groupsDict.values():
        for letter in letterList:
            alphabetDict[letter] = alphabetDict[letter] + 1
        # Convert the result to an array so its easy to sum up.
        convertToArr = list(alphabetDict.values())
        
        sumOfArr = np.sum(convertToArr)
        
        freqPercents = convertToArr/sumOfArr
        
        # Add the populated list to the group list
        groupFreqsList.append(copy.deepcopy(freqPercents))
        
        # reset the dictionary for the next run.
        alphabetDict = dict.fromkeys(string.ascii_uppercase, 0)

    return groupFreqsList

def getKey(groupFreqList, englishLetterFreqs):
    key = []
    maxVal = 0
    shiftVal = 0

    for group in groupFreqList:
        # Reset for the next group
        maxVal = 0
        for i in range(26):
            # Move the values over to to the left and then multiply them.
            shiftedArr = np.roll(group, -i)
            sumVal = np.sum(shiftedArr * englishLetterFreqs)
            
            if (sumVal > maxVal):
                maxVal = sumVal
                shiftVal = i
            # Reset the value
            sumVal = 0
        # Append the max value since it will be apart of the key.
        key.append(shiftVal)
    return key

# Returns all of the factors of a number in a set.
def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(pow(n, 0.5) + 1)) if n % i == 0)))

def main():
    cipher = None
    decipheredText = ''
    keyLength = None
    letterKey = None
    key = None
    
    # Holds the occurances of the factors, helps in finding the key.
    factorsFreqsDict = None
    dupsDict = None
    groupsDict = None

    # Holds the frequencies of each english alphabet. Frequencies are in alphabetic order.
    englishLetterFreqs = np.loadtxt(sys.path[0] + r'\data\englishLetterFreqs.txt')/100
    
    # This list holds the averaged values of each cipher group.
    groupPercentsList = None

    # Loads the cipher text from the file.
    with open(sys.path[0] + r'\data\vigenereCipher.txt', 'r') as myfile:
        cipher = myfile.read().replace('\n', '')
    
    # Gets the count of duplicate cipher texts of size 3
    dupsDict = getAllDups(cipher, 3)
    
    # Counts the frequencies of the factors, So I can decide on what size the key will be.
    factorsFreqsDict = getFactors(cipher, dupsDict)
    
    # Get the length of key which is of size 5 in this case.
    keyLength = factorsFreqsDict[5]
    
    print("Cipher Text:\n", cipher)
    
    # Creates the groups of cipher letter based on the key of size 5.
    groupsDict = createGroups(cipher, keyLength)

    groupPercentsList = getGroupPrecents(cipher, groupsDict)
    
    # This method will get the key by using the group percents and comparing their frquencies to the letter frequencies.
    key = getKey(groupPercentsList, englishLetterFreqs)
    
    # Deep copy the key so we do not mess with the original one.
    letterKey = copy.deepcopy(key)

    for i in range(len(key)): 
        letterKey[i] = chr(letterKey[i] + 65)
    
    print("Key:\n ", letterKey)

    # This for loop below goes through each letter in the cipher text and decodes it using the key.
    index = 0
    for cipherLetter in cipher:
        # If the index is greater than 4 than reset since we don't want to be larger than our key which is 5.
        if (index > 4):
            index = 0
        temp = ord(cipherLetter) - 64 
        temp = ((temp - key[index]) % 26) + 64
        decipheredText = decipheredText + chr(temp)
        index += 1
    decipheredText = decipheredText.replace('@', 'Z')
    
    print("Deciphered Text: \n" + decipheredText)


if __name__ == '__main__':
    main()