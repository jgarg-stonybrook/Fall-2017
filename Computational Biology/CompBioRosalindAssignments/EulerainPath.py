import sys
sys.setrecursionlimit(4000)

def start(dibruin,startpath,edgeMap):
    for key in startpath.keys():
        if startpath[key] == 1:
            ans = list()
            visited = dict()
            startTraversing(dibruin , str(key), edgeMap, ans)
            return ans

def startTraversing(dibruin , source , edgeMap , ans):
    flag = 0
    ans.append(source)
    if dibruin.__contains__(source):
        for nextVer in dibruin.get(source):
            tup = (source,nextVer)
            if edgeMap.__contains__(tup) == True:
                edgeMap.remove(tup)
                check = isValid(dibruin,nextVer,edgeMap)
                if check == False:
                    edgeMap.add(tup)
                else:
                    flag = 1
                    startTraversing(dibruin, nextVer, edgeMap, ans)

        if flag == 0:
            for nextVer in dibruin.get(source):
                tup = (source, nextVer)
                if tup in edgeMap == True:
                    edgeMap.remove(tup)
                    isValid(dibruin,nextVer,edgeMap)

def isValid(dibruin,nextVer,edgeMap):
    totalNodesLeftSet = set()
    for singleEdge in edgeMap:
        totalNodesLeftSet.add(singleEdge[0])
        totalNodesLeftSet.add(singleEdge[1])
    canBeVisitedNodesSet = set()
    traverseFromNode(dibruin,edgeMap,canBeVisitedNodesSet,nextVer)
    if canBeVisitedNodesSet == totalNodesLeftSet:
        return True
    else:
        return False

def traverseFromNode(dibruin,edgeMap,canBeVisitedNodesSet,nextVer):
    canBeVisitedNodesSet.add(nextVer)
    if nextVer in dibruin.keys():
        for nextNode in dibruin.get(nextVer):
            tup = (nextVer, nextNode)
            if edgeMap.__contains__(tup) == True:
                if nextNode not in canBeVisitedNodesSet:
                    traverseFromNode(dibruin,edgeMap,canBeVisitedNodesSet,nextNode)

def printAns(ans):
    print("->".join(ans))

def appendLast(startpath,ans):
    for key in startpath.keys():
        if startpath[key] == -1:
            ans.append(key)
            return ans

def readFile(path):
    file = open(path, "r")
    startpath = dict()
    dibruin = dict()
    edgeMap = set()
    for line in (file):
        read = line.strip()
        edge = read.split(" ")
        if dibruin.__contains__(edge[0]) == False:
            next = edge[2].split(",")
            dibruin[edge[0]] = next
            if startpath.__contains__(edge[0]) == False:
                startpath[edge[0]] = len(next)
            else:
                startpath[edge[0]] += len(next)
            for val in next:
                if startpath.__contains__(val) == False:
                    startpath[val] = -1
                else:
                    startpath[val] -= 1
                singleEdge = (edge[0],val)
                if edgeMap.__contains__(singleEdge) == False:
                    edgeMap.add(singleEdge)
    file.close()
    return dibruin,startpath,edgeMap

dibruin,startpath,edgeMap = readFile("/Users/jatingarg/Downloads/rosalind_ba3g (1).txt")
ans = start(dibruin,startpath,edgeMap)
appendLast(startpath,ans)
printAns(ans)