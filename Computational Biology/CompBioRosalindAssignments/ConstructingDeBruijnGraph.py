charRev = {'A':'T',
           'T':'A',
           'C':'G',
           'G':'C'}

def makedeBruijn(readSet):
    reverseSet = set()
    for read in readSet:
        reverseSet.add(produceReverseComp(read))

    kminus1merList = dict()
    for read in readSet:
        kminus1merList[((read[:len(read)-1],read[1:len(read)]))] = 1

    for read in reverseSet:
        kminus1merList[((read[:len(read) - 1], read[1:len(read)]))] = 1

    return kminus1merList

def produceReverseComp(read):
    rev = str()
    for char in read:
        rev += (charRev.get(char))
    return rev[::-1]

def readFile(path):
    file = open(path, "r")
    readSet = set()
    for line in (file):
        read = line.strip()
        readSet.add(read)
    file.close()
    return readSet

def printAns(ans):
    for key in ans.keys():
        str = "(" + key[0] + ", " + key[1] + ")"
        print(str)

readSet = readFile("/Users/jatingarg/Downloads/rosalind_dbru.txt")
ans = makedeBruijn(readSet)
printAns(ans)