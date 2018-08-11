charRev = {'A':'T',
           'T':'A',
           'C':'G',
           'G':'C'}

def error_correct(readDict):
    correct = set()
    incorrect = set()
    for read in readDict.keys():
        if readDict.get(read) >= 2 or (readDict.get(read) == 1 and readDict.__contains__(produceReverseComp(read))):
            correct.add(read)
            continue
        else:
            incorrect.add(read)
            continue

    ans = list()
    for iread in incorrect:
        for read in correct:
            if getEditDistance(iread,read) == True:
                ans.append((iread, read))
                break
            elif getEditDistance(iread,produceReverseComp(read)) == True:
                ans.append((iread,produceReverseComp(read)))
                break

    return ans

def getEditDistance(first,second):
    count = 0
    for i in range(len(first)):
        if first[i] != second[i]:
            count += 1
        if count == 2:
            return False
    return True

def produceReverseComp(read):
    rev = str()
    for char in read:
        rev += (charRev.get(char))
    return rev[::-1]


def readFile(path):
    file = open(path, "r")
    count = 0
    readDict = dict()
    for line in (file):
        if line.strip().__contains__(">"):
            continue
        else:
            read = line.strip()
            if readDict.__contains__(read) == False:
                readDict[read] = 1
            else:
                readDict[read] += 1
    file.close()
    return readDict

def printAns(ans):
    for i in range(len(ans)):
        s = ans[i][0] + "->" + ans[i][1]
        print(s)

readDict = readFile("/Users/jatingarg/Downloads/rosalind_corr (1).txt")
ans = error_correct(readDict)
printAns(ans)