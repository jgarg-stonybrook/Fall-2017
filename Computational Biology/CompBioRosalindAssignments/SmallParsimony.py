totalCost = 0
class TreeNode(object):

    def __init__(self,num,taxa=None):

        self.nodeNum = num
        self.dnaSequence = taxa
        self.leftChild = None
        self.rightChild = None
        self.cost = 0


def readFile(path):
    file = open(path, "r")
    startpath = dict()
    tree = dict()
    count = 0
    numLeaf = 0
    root = 0
    for line in (file):
        read = line.strip()
        if count == 0:
            numLeaf = int(read)
            count += 1
            continue

        if count <= numLeaf:
            parent , child = read.split("->")
            lis = list()
            for ch in child:
                charSet = set(ch)
                lis.append(charSet)
            if tree.__contains__(int(parent)) == False:
                parentNode = TreeNode(int(parent), list())
                childNode = TreeNode(count-1,lis)
                parentNode.leftChild = childNode
                tree[count-1] = childNode
                tree[int(parent)] = parentNode
            else:
                parentNode = tree.get(int(parent))
                childNode = TreeNode(count - 1, lis)
                parentNode.rightChild = childNode
                tree[count - 1] = childNode

            count += 1
            root = int(parent)
        else:
            parent, child = read.split("->")
            parent = int(parent)
            child = int(child)
            if tree.__contains__(parent) == False:
                parentNode = TreeNode(parent, list())
                childNode = tree.get(child)
                parentNode.leftChild = childNode
                tree[parent] = parentNode
            else:
                parentNode = tree.get(parent)
                childNode = tree.get(child)
                parentNode.rightChild = childNode
            count += 1
            root = parent

    file.close()
    return tree,root

def traversePostOrder(root):

    if root is None:
        return

    traversePostOrder(root.leftChild)
    traversePostOrder(root.rightChild)
    if root.leftChild is None or root.rightChild is None:
        return

    dnaSeqList = root.dnaSequence
    leftDnaList = root.leftChild.dnaSequence
    rightDnaList = root.rightChild.dnaSequence
    for i in range(len(leftDnaList)):
        intersect = leftDnaList[i].intersection(rightDnaList[i])
        union = leftDnaList[i].union(rightDnaList[i])
        if len(intersect) == 0:
            dnaSeqList.append(union)
        else:
            dnaSeqList.append(intersect)

def traversePreOrder(root,val,parentSeq):
    global totalCost
    if root is None:
        return

    if root.leftChild is None and root.rightChild is None:
        for i in range(len(root.dnaSequence)):
            for j in root.dnaSequence[i]:
                root.dnaSequence[i] = j
                if j != parentSeq[i]:
                    root.cost += 1
                    totalCost += 1
        return

    if root.nodeNum == val:
        for i in range(len(root.dnaSequence)):
            for j in root.dnaSequence[i]:
                root.dnaSequence[i] = j
                break

    else:
        for i in range(len(root.dnaSequence)):
            flag = 1
            for j in root.dnaSequence[i]:
                if j == parentSeq[i]:
                    flag = 0
                    root.dnaSequence[i] = parentSeq[i]
                    break
            if flag  == 1:
                root.cost += 1
                totalCost += 1
                for j in root.dnaSequence[i]:
                    root.dnaSequence[i] = j
                    break


    traversePreOrder(root.leftChild,val,root.dnaSequence)
    traversePreOrder(root.rightChild,val,root.dnaSequence)

def printAns(root,val):
    global totalCost

    if root.nodeNum == val:
        print(totalCost)

    if root.leftChild is None and root.rightChild is None:
        return

    left = "".join(root.dnaSequence) + "->" + "".join(root.leftChild.dnaSequence) + ":" + str(root.leftChild.cost)
    leftOpposite = "".join(root.leftChild.dnaSequence) + "->" + "".join(root.dnaSequence) + ":" + str(root.leftChild.cost)

    right = "".join(root.dnaSequence) + "->" + "".join(root.rightChild.dnaSequence) + ":" + str(root.rightChild.cost)
    rightOpposite = "".join(root.rightChild.dnaSequence) + "->" + "".join(root.dnaSequence) + ":" + str(root.rightChild.cost)

    print(left)
    print(leftOpposite)
    print(right)
    print(rightOpposite)

    printAns(root.leftChild,val)
    printAns(root.rightChild,val)


tree, root = readFile("/Users/jatingarg/Downloads/rosalind_ba7f.txt")
traversePostOrder(tree.get(root))
traversePreOrder(tree.get(root),root,"")
printAns(tree.get(root),root)