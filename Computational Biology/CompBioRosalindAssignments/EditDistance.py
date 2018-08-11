def editDistance(a,b):
    aLength = len(a)
    bLength = len(b)

    dp = [[0 for x in range(bLength+1)] for y in range(aLength+1)]
    for i in range(aLength+1):
        dp[i][0] = getGapCost() * i
    for j in range(bLength+1):
        dp[0][j] = getGapCost() * j

    ans = 0
    for i in range(1,aLength+1):
        for j in range(1,bLength+1):
            dp[i][j] = min(dp[i-1][j-1]+getMismatchCost(a[i-1],b[j-1]) , getGapCost()+dp[i-1][j] , getGapCost()+dp[i][j-1])

    aligx = ""
    aligy = ""
    index = 0

    count = 0
    x = aLength
    y = bLength
    while x > 0 or y > 0:
        if dp[x][y] == dp[x-1][y] + getGapCost():
            aligx += a[x-1]
            aligy += "-"
            x -= 1
            ans += 1
        elif dp[x][y] == dp[x][y-1] + getGapCost():
            aligx += "-"
            aligy += b[y-1]
            y -= 1
            ans += 1
        elif dp[x][y] == dp[x-1][y-1] + getMismatchCost(a[x-1],b[y-1]):
            aligx += a[x-1]
            aligy += b[y-1]
            if getMismatchCost(a[x-1],b[y-1]) != 0:
                ans += 1
            x -= 1
            y -= 1
        count += 1
    print(ans)
    print(aligx[::-1])
    print(aligy[::-1])

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

tupl = readFile("/Users/jatingarg/Downloads/rosalind_edta (1).txt")
editDistance(tupl[0],tupl[1])