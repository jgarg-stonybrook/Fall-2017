def LFMapping(lColumn,num):
    fColumn = "".join(sorted(lColumn))
    lDict = {
        "$" : 0,
        "A" : 0,
        "C" : 0,
        "T" : 0,
        "G" : 0
    }
    fDict = {
        "$": 0,
        "A": 0,
        "C": 0,
        "T": 0,
        "G": 0
    }
    lList = list()
    fList = list()

    for i in range(len(lColumn)):
        lList.append((lColumn[i],lDict.get(lColumn[i])))
        lDict[lColumn[i]] += 1

    for i in range(len(fColumn)):
        fList.append((fColumn[i],fDict.get(fColumn[i])))
        fDict[fColumn[i]] += 1

    toSearch = lList[num]

    for i in range(len(fColumn)):
        if fList[i] == toSearch:
            return i


def readFile(path):
    file = open(path, "r")
    count = 0
    dnaSequence = ""
    num = 0
    for line in (file):
        if count == 0:
            dnaSequence = line.strip()
        else:
            num = line.strip()
        count += 1

    file.close()
    return dnaSequence,num

# print(LFMapping("T$GACCA",3))
tupl = readFile("/Users/jatingarg/Downloads/rosalind_ba9k.txt")
print(LFMapping(tupl[0],int(tupl[1])))