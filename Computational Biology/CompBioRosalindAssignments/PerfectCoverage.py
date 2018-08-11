charRev = {'A':'T',
           'T':'A',
           'C':'G',
           'G':'C'}

def deBruijntraversing(readDict,source,target):
    visited = set()
    travList = list()
    deBruijntraversingUtil(readDict,source,target,visited,travList)
    return travList

def deBruijntraversingUtil(readDict,source,target,visited,travList):
    stack = list()
    stack.append(source)
    travList.append(source)
    visited.add(source)
    while len(stack) > 0:
        source = stack.pop()
        for nextNode in readDict.get(source):
            if nextNode == target:
                return travList
            else:
                if visited.__contains__(nextNode) == False:
                    stack.append(nextNode)
                    travList.append(nextNode)
                    visited.add(nextNode)
            visited.remove(nextNode)


def converge(travList):
    temp = travList[0]
    for read in travList[1:]:
        temp += read[len(read)-1]
    return temp

def joinEndStart(genome):
    temp = [0 for i in range(len(genome))]
    prev = 0
    for i in range(1,len(genome)):
        if genome[prev] == genome[i]:
            prev += 1
            temp[i] = prev
        else:
            while(genome[i] != genome[prev] and prev > 0):
                prev = temp[prev-1]
            if genome[i] == genome[prev]:
                prev += 1
                temp[i] = prev
    return temp[len(genome)-1]

def readFile(path):
    file = open(path, "r")
    readDict = dict()
    count = 0
    source = str()
    for line in (file):
        read = line.strip()
        if count == 0:
            source = read[0:len(read)-1]
            count += 1
        leftkminus1 = read[0:len(read)-1]
        rightkmins1 = read[1:len(read)]
        if readDict.__contains__(leftkminus1) == False:
            temp = list()
            temp.append(rightkmins1)
            readDict[leftkminus1] = temp
        else:
            temp = readDict.get(leftkminus1)
            temp.append(rightkmins1)
            readDict[leftkminus1] = temp
    file.close()
    return readDict,source

def printAns(genome,count):
    print(genome[:len(genome)-count])

readDict,source = readFile("/Users/jatingarg/Downloads/rosalind_pcov.txt")
travList = deBruijntraversing(readDict,source,source)
genome = converge(travList)
count = joinEndStart(genome)
printAns(genome , count)