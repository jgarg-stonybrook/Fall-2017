#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

import time

distanceDict = dict()
excludeList = list()
nodes = 0
fcnodes = 0
cpnodes = 0

#Your backtracking function implementation
def BT(L, M):
    "*** YOUR CODE HERE ***"
    if L < 0 or M <= 0:
        return -1,[]
    ans = list()
    state = list()
    maxL = L
    # Here solution is finded for lengths starting from L,L-1 until a optimal solution is founded
    for i in range(L,-1,-1):
        distanceDict.clear()
        state.clear()
        tem = recursiveBackTracking(state, i, 0, M,maxL)
        # If solution is not founded for particular length, then we break
        if tem[0] == -1:
            break
        ans.append(tem)
    if len(ans) == 0:
        return -1,[]
    return ans[-1]

def recursiveBackTracking(state,L,nextMin,M,maxL):
    global nodes
    nodes += 1
    # if len of sol reaches the M, then solution is founded and it is returned
    if len(state) == M:
        distanceDict.clear()
        return ([max(state), state.copy()])
    # Values are assigned from domain i,e from nextmin possible to L
    for nextPossible in range(nextMin,L+1):
        if len(state) == 0 and nextPossible >= 1:
            return -1,[]
        assignVar = nextPossible
        nextMin = assignVar+1
        state.append(assignVar)
        # If the state is consistent then we proceed with this value
        if consistent(state) == 1:
            # Recursion for next variable
            tempans = recursiveBackTracking(state,L,nextMin,M,maxL)
            # Here condition is enforced so that solution for inputted L is found first before proceeding for optimal sol
            if tempans[0] != -1:
                maxi = max(tempans[1])
                if L < maxL:
                    return tempans
                elif L == maxL:
                    if maxi == maxL:
                        return tempans
            state.pop(-1)
            removeFromDistDic(assignVar,state)
        else:
            popped = state.pop(-1)
    return -1,[]

def consistent(state):
    # Function for checking consistency of assigning value to a variable
    if distanceDict.__len__() == 0:
        distanceDict[0] = 1
        return 1
    else:
        last = state[-1]
        temp = list()
        for var in range(len(state)-1):
            # Adding distances to the dictionary so that we can check them fast next time
            if distanceDict.__contains__(abs(last-state[var]))and distanceDict.get(abs(last-state[var])) == 1:
                return -1
            else:
                if temp.__contains__(abs(last-state[var])):
                    return  -1
                temp.append(abs(last-state[var]))
        for var in range(len(state) - 1):
            distanceDict[abs(last-state[var])] = 1
        return 1


def removeFromDistDic(popped,state):
    # Function for removing values from dictionary so that we can loop for next value of same variable
    for var in range(len(state)):
        if distanceDict.__contains__(abs(popped - state[var])) and distanceDict.get(abs(popped - state[var])) == 1:
            distanceDict[abs(popped-state[var])] = 0

#Your backtracking+Forward checking function implementation
def FC(L, M):
    "*** YOUR CODE HERE ***"
    if L < 0 or M <= 0:
        return -1,[]
    ans = list()
    state = list()
    fcList = list()
    maxL = L
    # Here solution is finded for lengths starting from L,L-1 until a optimal solution is founded
    for i in range(L,-1,-1):
        distanceDict.clear()
        state.clear()
        fcList.clear()
        tem = recursiveBackTrackingWithFC(state, i, 0, M,fcList,maxL)
        # If solution is not founded for particular length, then we break
        if tem[0] == -1:
            break
        ans.append(tem)
    if len(ans) == 0:
        return -1,[]
    return ans[-1]


def recursiveBackTrackingWithFC(state, L, nextMin, M,fcList,maxL):
    global fcnodes
    fcnodes += 1
    # if len of sol reaches the M, then solution is founded and it is returned
    if len(state) == M:
        distanceDict.clear()
        return ([max(state), state.copy()])

    if nextMin == -1:
        return -1,[]
    # Values are assigned from domain i,e from nextmin possible to L
    for nextPossible in range(nextMin, L + 1):
        if len(state) == 0 and nextPossible >= 1:
            return -1,[]
        if nextPossible in fcList:
            continue
        assignVar = nextPossible
        nextMin = assignVar + 1
        state.append(assignVar)
        # If the state is consistent then we proceed with this value
        if consistent(state) == 1:
            fcList,temp,nextAllowed = addValuesToBeRemoved(nextPossible,fcList,L)
            # Condition to not do recusrion for values that are removed by forward chekcing
            if nextAllowed == -1 and len(state) < M:
                state.pop(-1)
                removeFromDistDic(assignVar, state)
                fcList = removeFromFCList(fcList.copy(), temp)
            else:
                # Recursion for next variable
                tempans = recursiveBackTrackingWithFC(state, L, nextAllowed, M,fcList.copy(),maxL)
                # Here condition is enforced so that solution for inputted L is found first before proceeding for optimal sol
                if tempans[0] != -1:
                    maxi = max(tempans[1])
                    if L<maxL:
                        return tempans
                    elif L == maxL:
                        if maxi == maxL:
                            return tempans
                state.pop(-1)
                removeFromDistDic(assignVar, state)
                fcList = removeFromFCList(fcList.copy(),temp)
        else:
            popped = state.pop(-1)
    return -1,[]


def addValuesToBeRemoved(nextPossible,fcList,L):
    # Function to make a list which are removed from domain in forward checking
    temp = list()
    count = 0
    nextAllowed = -1
    for i in range(nextPossible+1,L+1):
        if distanceDict.__contains__(abs(i - nextPossible)) and distanceDict.get(abs(i - nextPossible)) == 1:
                if fcList.__contains__(i) == False:
                    fcList.append(i)
                    temp.append(i)
        else:
            if count == 0:
                nextAllowed = i
                count += 1
    return fcList,temp,nextAllowed

def removeFromFCList(fcList,temp):
    # Function for adding the removed values in domain so that we can loop for next value for same variable
    for i in temp:
        if i in fcList:
            fcList.remove(i)
    return fcList

#Bonus: backtracking + constraint propagation
def CP(L, M):
    "*** YOUR CODE HERE ***"
    if L < 0 or M <= 0:
        return -1,[]
    ans = list()
    state = list()
    fcList = list()
    maxL = L
    # Here solution is finded for lengths starting from L,L-1 until a optimal solution is founded
    for i in range(L,-1,-1):
        distanceDict.clear()
        state.clear()
        fcList.clear()
        tem = recursiveBackTrackingWithCP(state, i, 0, M,fcList,maxL)
        # If solution is not founded for particular length, then we break
        if tem[0] == -1:
            break
        ans.append(tem)
    if len(ans) == 0:
        return -1,[]
    return ans[-1]


def recursiveBackTrackingWithCP(state, L, nextMin, M,fcList,maxL):
    global cpnodes
    cpnodes += 1
    # if len of sol reaches the M, then solution is founded and it is returned
    if len(state) == M:
        return ([max(state), state.copy()])

    if nextMin == -1:
        return -1,[]
    # Values are assigned from domain i,e from nextmin possible to L
    for nextPossible in range(nextMin, L + 1):
        if len(state) == 0 and nextPossible >= 1:
            return -1,[]
        if nextPossible in fcList:
            continue
        assignVar = nextPossible
        nextMin = assignVar + 1
        state.append(assignVar)
        # If the state is consistent then we proceed with this value
        if consistent(state) == 1:
            fcList,temp,nextAllowed,allowedCount = addValuesToBeRemovedCP(nextPossible,fcList,L)
            # Condition to not do recusrion for values that are removed by forward chekcing plus the consistenct in CP
            if nextAllowed == -1 and len(state) < M:
                state.pop(-1)
                removeFromDistDic(assignVar, state)
                fcList = removeFromCPList(fcList.copy(), temp)
            elif allowedCount < M - len(state):
                state.pop(-1)
                removeFromDistDic(assignVar, state)
                fcList = removeFromCPList(fcList.copy(), temp)
            else:
                # Recursion for next variable
                tempans = recursiveBackTrackingWithCP(state, L, nextAllowed, M,fcList.copy(),maxL)
                # Here condition is enforced so that solution for inputted L is found first before proceeding for optimal sol
                if tempans[0] != -1:
                    maxi = max(tempans[1])
                    if L<maxL:
                        return tempans
                    elif L == maxL:
                        if maxi == maxL:
                            return tempans
                state.pop(-1)
                removeFromDistDic(assignVar, state)
                fcList = removeFromCPList(fcList.copy(),temp)
        else:
            popped = state.pop(-1)
    return -1,[]

def addValuesToBeRemovedCP(nextPossible,fcList,L):
    # Function to remove values and propagate for values according to constraint propagation
    temp = list()
    count = 0
    nextAllowed = -1
    allowedCount = 0
    for i in range(nextPossible+1,L+1):
        if distanceDict.__contains__(abs(i - nextPossible)) and distanceDict.get(abs(i - nextPossible)) == 1:
                if fcList.__contains__(i) == False:
                    fcList.append(i)
                    temp.append(i)
        else:
            allowedCount += 1
            if count == 0:
                nextAllowed = i
                count += 1
    return fcList,temp,nextAllowed,allowedCount


def removeFromCPList(fcList,temp):
    # Adding the removed values again
    for i in temp:
        if i in fcList:
            fcList.remove(i)
    return fcList

start_time = time.time()
print(BT(25,6))
print("Nodes expanded in BT: ",nodes)
print("---BT took %.9s seconds ---" % (time.time() - start_time))
start_time = time.time()
print(FC(25,6))
print("---FC took %.9s seconds ---" % (time.time() - start_time))
print("Nodes expanded in FC: ",fcnodes)
start_time = time.time()
print(CP(25,6))
print("---CP took %.9s seconds ---" % (time.time() - start_time))
print("Nodes expanded in CP: ",cpnodes)