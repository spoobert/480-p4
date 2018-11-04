from abFLOPSY import abFlopsy, abMiniMax
from FLOPSY import Flopsy, minMax
import time

def getBoardArr(fileName):
    with open(fileName) as f:
        tmp = [[ int(char) for char in line.split()] for line in f]
    oneC,twoC = (0,0)
    for line in tmp:
        for char in line:
            if char == 1:
                oneC+=1
            elif char == 2:
                twoC+=1
    if oneC != twoC:
        return False
    else: return tmp

def main():

    while(True):
        b = getBoardArr('zeroboard.txt')
        if not b:
            print('Bad Board! *DANGER* TRY AGAIN...')
            continue
        AB = int(input('1 for MiniMax , 2 for Alpha Beta ...'))
        if AB == 1:
            F = Flopsy(b)
            res = minMax(F)
            print('select move: ',res.move,' found at depth: ',minMax.count())
        if AB == 2:
            F = abFlopsy(b)
            res = abMiniMax(F)
            from abFLOPSY import herdSize
            print('select move: ',res.move,' ...expanded: ',herdSize)

        input('waiting...')

if __name__=="__main__":
    main()