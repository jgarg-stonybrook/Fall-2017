lList = list()
fList = list()

fDict = {
    "$": 0,
    "A": 0,
    "C": 0,
    "T": 0,
    "G": 0
}

chMapping = {
    "$": 1,
    "A": 2,
    "C": 3,
    "G": 4,
    "T": 5
}

def getFirstColumn(lColumn):
    return "".join(sorted(lColumn))

def generateLFMapper(lColumn):
    tup = ('',0,0, 0, 0, 0)
    lList.append(tup)
    for i in range(1,len(lColumn)+1):
        temp = list()
        num = chMapping.get(lColumn[i-1])
        lasttup = lList[i-1]
        temp.append(lColumn[i-1])
        for j in range(1,6):
             if j == num:
                temp.append(lasttup[j] + 1)
             else:
                temp.append(lasttup[j])
        lList.append(tuple(temp))
    lList.pop(0)

def BWMATCHING(lastColumn, pattern):
    top = 0
    bottom = len(lastColumn)-1
    while top <= bottom:
        if pattern != "":
            symbol = pattern[-1]
            pattern = pattern[0:len(pattern)-1]

            first = lList[top]
            last = lList[bottom]
            start = first[chMapping.get(symbol)]
            end = last[chMapping.get(symbol)]

            if lastColumn[top] == symbol:
                start -= 1

            times = end - start
            if times >= 1:
                top = fList[chMapping.get(symbol)-1] + start
                bottom = fList[chMapping.get(symbol)-1] + end - 1
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

def constructFirstOccurence(firstColumn):
    for i in range(len(firstColumn)):
        if fDict.get(firstColumn[i]) == 0:
            fDict[firstColumn[i]] = 1
            fList.append(i)

tupl = readFile("/Users/jatingarg/Downloads/rosalind_ba9m.txt")
lC = tupl[0]
fC = getFirstColumn(lC)
constructFirstOccurence(fC)
generateLFMapper(lC)
ans = list()
for element in tupl[1]:
    pattern = element
    a = str(BWMATCHING(lC,pattern))
    ans.append(a)
print(" ".join(ans))