import pickle
from random import randint

def selectDict(data, length):
    index = 0
    maxLen = len(data[len(data)-1][0].split())
    minLen = len(data[0][0].split())

    if maxLen<length:
        maxlen=str(maxLen)
        raise IndexError("length too long : "+maxLen+" max expected")
    elif minLen>length:
        minLen=str(minLen)
        raise IndexError("length too short : "+minLen+" min expected")

    for i in range(len(data)):
        if len(data[i][0].split())==length:
            index = i
    return index


def selectSeedFromDict(data, output, number, index):
    seed = []
    max = len(data[index])
    for i in range(number):
        index_sample = randint(0,max-1)
        seed.append(data[index][index_sample])

    with open(output, 'wb') as fp:
        pickle.dump(seed, fp)

    return seed

def selectPhrases(file, length=2, number=1):
    data = pickle.load(open(file, 'rb'))
    LENGTH = range(2, len)
    NUMBER = 200
    for len in LENGTH:
        OUTPUT = "./SelectedPhrases/Phrases_" + str(len) + "_" + str(NUMBER) + ".txt"
        index = selectDict(data, length=len)  # select dictionary depending on phrase length
        seed = selectSeedFromDict(data, output=OUTPUT, number=number, index=index)  # return 'number' phrases of the dict at the 'index'
    return seed

def generateSEED(minlength=2, maxlength=18, length=8, output="./test.txt"):
    LENGTH = range(minlength, maxlength)
    NUMBER = 200
    for leng in LENGTH:
        input = []
        output = []
        FILE = "./SelectedPhrases/Phrases_" + str(leng) + "_" + str(NUMBER) + ".txt"
        INPUT_FILE = "./Seeds/input_" + str(leng) + "_" + str(NUMBER) + "_" + str(length) + ".txt"
        OUTPUT_FILE = "./Seeds/output" + str(leng) + "_" + str(NUMBER) + "_" + str(length) + ".txt"
        data = pickle.load(open(FILE, 'rb'))
        for phrase in data:
            input.append(phrase.split()[:length])
            output.append(phrase.split()[length:])

        with open(INPUT_FILE, 'wb') as fp:
            pickle.dump(input, fp)
        with open(OUTPUT_FILE, 'wb') as fp:
            pickle.dump(output, fp)

"""--------------------------------------------------"""
SORTED_FILE = "./SortedData.txt"
FILE = "./Seeds/input_2_200_3.txt"
#generateSEED(length=3)

data = pickle.load(open(FILE, 'rb'))
print(data)