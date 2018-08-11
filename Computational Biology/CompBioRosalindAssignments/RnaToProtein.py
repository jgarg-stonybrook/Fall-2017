proteinToRna = {'GCT': 'A',
                'GCC': 'A',
                'GCA': 'A',
                'GCG': 'A',
                'TTA': 'L',
                'TTG': 'L',
                'CTT': 'L',
                'CTC': 'L',
                'CTA': 'L',
                'CTG': 'L',
                'CGT': 'R',
                'CGC': 'R',
                'CGA': 'R',
                'CGG': 'R',
                'AGA': 'R',
                'AGG': 'R',
                'AAA': 'K',
                'AAG': 'K',
                'AAT': 'N',
                'AAC': 'N',
                'ATG': 'M',
                'GAT': 'D',
                'GAC': 'D',
                'TTT': 'F',
                'TTC': 'F',
                'TGT': 'C',
                'TGC': 'C',
                'CCT': 'P',
                'CCC': 'P',
                'CCA': 'P',
                'CCG': 'P',
                'CAA': 'Q',
                'CAG': 'Q',
                'TCT': 'S',
                'TCC': 'S',
                'TCA': 'S',
                'TCG': 'S',
                'AGT': 'S',
                'AGC': 'S',
                'GAA': 'E',
                'GAG': 'E',
                'ACT': 'T',
                'ACC': 'T',
                'ACA': 'T',
                'ACG': 'T',
                'GGT': 'G',
                'GGC': 'G',
                'GGA': 'G',
                'GGG': 'G',
                'TGG': 'W',
                'CAT': 'H',
                'CAC': 'H',
                'TAT': 'Y',
                'TAC': 'Y',
                'ATT': 'I',
                'ATC': 'I',
                'ATA': 'I',
                'GTT': 'V',
                'GTC': 'V',
                'GTA': 'V',
                'GTG': 'V',
                'TAA': 'STOP',
                'TGA': 'STOP',
                'TAG': 'STOP'
                }



def rnaToProtein(rna):
    mrna = str(rna)
    newmrna = mrna.replace('U','T')
    return convertMrnatoProtein(newmrna)

def convertMrnatoProtein(dnaSequence):
    protein = []
    for x in range(0,len(dnaSequence),3):
        pro = proteinToRna.get(dnaSequence[x:x + 3])
        if(pro != 'STOP'):
            protein.append(pro)
        else:
            break
    return "".join(protein)

def readFile(path):
        file = open(path, "r")
        count = 0
        dnaSequencelst = []
        for line in (file):
            dnaSequencelst.append(line.strip())

        file.close()
        return "".join(dnaSequencelst)

print(rnaToProtein(readFile("/Users/jatingarg/Downloads/rosalind_prot.txt")))