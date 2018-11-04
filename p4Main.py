from abFLOPSY import *
import time
#from abFLOPSY import *
def getBoardArr(fileName):
    with open(fileName) as f:
        return [[ int(char) for char in line.split()] for line in f]

def main():
    b = getBoardArr('oboard.txt')
    F = abFlopsy(b,True,'root',0)
    res = abMinMax(F,float('-inf'),float('inf'))
    print(res.move,' ',abMinMax.count(),' cpuTime: ',time.clock() - abMinMax.timer)

if __name__=="__main__":
    main()