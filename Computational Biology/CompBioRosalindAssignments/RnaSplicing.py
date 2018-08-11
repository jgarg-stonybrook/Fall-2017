import re
class RnaSplicing():


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

    def readFile(self,path):
        file = open(path, "r")
        count = 0
        dnaSequencelst = []
        introns = []
        for line in (file):
            if line.startswith('>'):
                count += 1
            else:
                if count == 1:
                    dnaSequencelst.append(line.strip())
                else:
                    introns.append(line.strip())
        file.close()
        return "".join(dnaSequencelst),introns

    def separateIntrons(self,dnaSequence,introns):
        newString = []
        newString.append(dnaSequence)
        count = 0
        for intron in introns:
            newString.append(self.separateIntronUtil(intron,newString[count]))
            count+=1
        return newString[count]

    def separateIntronUtil(self,intron,dnaSequence):
        newString = ""
        st = 0
        for ind in re.finditer(intron,dnaSequence):
            lst = ind.start()
            newString += dnaSequence[st:lst]
            st = lst + len(intron)
        newString += dnaSequence[st:]
        return newString


    def convertMrnatoProtein(self,dnaSequence):
        protein = []
        for x in range(0,len(dnaSequence),3):
            pro = self.proteinToRna.get(dnaSequence[x:x + 3])
            if(pro != 'STOP'):
                protein.append(pro)
            else:
                break
        return "".join(protein)

obj = RnaSplicing()
dnaSequence, introns = obj.readFile("/Users/jatingarg/Downloads/rosalind_splc (1).txt")
extrons = obj.separateIntrons(dnaSequence,introns)
print(obj.convertMrnatoProtein(extrons))

