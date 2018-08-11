def BWT(dna):
    dnaLength = len(dna)
    rotateList = [dna[x-1:] + dna[0:x-1]  for x in range(len(dna))]

    rotateList = sorted(rotateList)

    bwt = [st[-1] for st in rotateList]
    return "".join(bwt)


print(BWT("ATTCG$"))