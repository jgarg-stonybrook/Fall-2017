lList = list()
fList = list()

lDict = {
    "$": 0,
    "A": 0,
    "C": 0,
    "T": 0,
    "G": 0
}

fDict = {
    "$": 0,
    "A": 0,
    "C": 0,
    "T": 0,
    "G": 0
}

def getFirstColumn(lColumn):
    return "".join(sorted(lColumn))

def generateLFMapper(lColumn,fColumn):
    for i in range(len(lColumn)):
        lList.append((lColumn[i],lDict.get(lColumn[i])))
        lDict[lColumn[i]] += 1

    for i in range(len(fColumn)):
        fList.append((fColumn[i],fDict.get(fColumn[i])))
        fDict[fColumn[i]] += 1

def LFMapping(lColumn,num):
    fColumn = getFirstColumn(lColumn)

    toSearch = lList[num]

    for i in range(len(fColumn)):
        if fList[i] == toSearch:
            return i

def BWMATCHING(lastColumn, pattern):
    top = 0
    bottom = len(lastColumn)-1
    while top <= bottom:
        if pattern != "":
            symbol = pattern[-1]
            pattern = pattern[0:len(pattern)-1]
            topIndex = -1
            bottomIndex = -1
            count = 0
            for i in range(top,bottom+1):
                element = lList[i]
                if element[0] == symbol:
                    if count == 0:
                        topIndex = i
                        count += 1
                    bottomIndex = i
            if topIndex != -1 and bottomIndex != -1:
                top = LFMapping(lastColumn,topIndex)
                bottom = LFMapping(lastColumn,bottomIndex)
            else:
                return 0
        else:
            return bottom-top+1


def readFile(path):
    file = open(path, "r")
    count = 0
    dnaSequence = ""
    lis = list()
    for line in (file):
        if line.strip().__contains__(" ") == False:
            dnaSequence += line.strip()
        else:
            lis.extend(line.strip().split(" "))

    file.close()
    return dnaSequence,lis


tupl = readFile("/Users/jatingarg/Downloads/rosalind_ba9l.txt")
lC = tupl[0]
fC = getFirstColumn(lC)
generateLFMapper(lC,fC)
ans = list()
for element in tupl[1]:
    pattern = element
    ans.append(str(BWMATCHING(lC,pattern)))
print(" ".join(ans))