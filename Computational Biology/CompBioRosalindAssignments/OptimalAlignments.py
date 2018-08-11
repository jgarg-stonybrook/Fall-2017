def editDistance(a,b):
    aLength = len(a)
    bLength = len(b)

    dp = [[0 for x in range(bLength+1)] for y in range(aLength+1)]
    ways = [[0 for x in range(bLength+1)] for y in range(aLength+1)]

    for i in range(aLength+1):
        dp[i][0] = getGapCost() * i
        ways[i][0] = 1
    for j in range(bLength+1):
        dp[0][j] = getGapCost() * j
        ways[0][j] = 1

    modulo = 134217727
    for i in range(1,aLength+1):
        for j in range(1,bLength+1):
            dp[i][j] = min(dp[i-1][j-1]+getMismatchCost(a[i-1],b[j-1]) , getGapCost()+dp[i-1][j] , getGapCost()+dp[i][j-1])
            if dp[i][j] == dp[i-1][j-1] + getMismatchCost(a[i-1],b[j-1]):
                ways[i][j] = (ways[i][j] + ways[i-1][j-1])% modulo
            if dp[i][j] == getGapCost()+ dp[i-1][j]:
                ways[i][j] = (ways[i][j] + ways[i-1][j])%modulo
            if dp[i][j] == getGapCost()+dp[i][j-1]:
                ways[i][j] = (ways[i][j] + ways[i][j-1])% modulo

    print(dp)
    print((ways[aLength][bLength])%modulo)

def getMismatchCost(a,b):
    if a == b:
        return 0
    else:
        return 1

def getGapCost():
    return 1

def readFile(path):
    file = open(path, "r")
    count = 0
    dnaSequence1 = ""
    dnaSequence2 = ""
    for line in (file):
        if line.strip().__contains__(">"):
            count += 1
        elif count == 1:
            dnaSequence1 += line.strip()
        elif count == 2:
            dnaSequence2 += line.strip()

    file.close()
    return dnaSequence1,dnaSequence2

# tupl = readFile("/Users/jatingarg/Downloads/rosalind_ctea.txt")
# editDistance(tupl[0],tupl[1])
editDistance("PLEASANTLY","MEANLY")