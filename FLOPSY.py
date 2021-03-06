from itertools import product
import collections
from perm import perm 


class Counter :
    def __init__(self, fun) :
        self._fun = fun
        self.counter=0
        import time
        self.timer = time.clock()

    def __call__(self,*args, **kwargs) :
        self.counter += 1
        return self._fun(*args, **kwargs)
    def count(self):
        return self.counter

# Flopsy represents the next chosen move in the game
# 'root' Flopsy is the initial game state
# Flopsy is mad at Mommy...Flopsy:= playerNot(Mommy.player) ; maxTurnNot(Mommy.maxTurn)
class Flopsy():
    def __init__(self, board, maxT=True, mv='root'):
        self.move = mv
        self.maxTurn = not maxT
        self.board = [ [p for p in line] for line in board ]
        if mv != 'root':
            self.board[mv[0]][mv[1]] = 1 if self.maxTurn else 2
        #swap i,j -> j,i to make row major order
        self.openSet = [ (i,j) for j,i in product( range(4), range(4)) if self.board[i][j] == 0 ]
        self.p1Count = sum( map(self.findPossiblePOne,perm) )
        self.p2Count = sum( map(self.findPossiblePTwo,perm) )
        # any(self.mapFindWinner(p) == 1 for p in perm)
        self.p1Won = True if [ p for p in map(self.mapFindWinner,perm) if p == 1] else False
        self.p2Won = True if [ p for p in map(self.mapFindWinner,perm) if p == 2] else False
        self.eval = self.staticEval()
    
    def isLeaf(self):
        if self.p1Won or self.p2Won:
            return True
        if self.openSet == []:
            return True
        return False 

    def staticEval(self):
        if self.p1Won:
            return 100
        if self.p2Won:
            return -100
        return self.p1Count - self.p2Count

    def mapFindWinner(self,p):
        return self.board[0][p[0]]&self.board[1][p[1]]&self.board[2][p[2]]&self.board[3][p[3]]
        
    def findPossiblePOne(self,p):
        res= self.board[0][p[0]]|self.board[1][p[1]]|self.board[2][p[2]]|self.board[3][p[3]]
        if res == 1:
            return 1
        return 0

    def findPossiblePTwo(self,p):
        res= self.board[0][p[0]]|self.board[1][p[1]]|self.board[2][p[2]]|self.board[3][p[3]]
        if res == 2:
            return 1
        return 0


    # 1. board positions -> add single move from open set
    # 2. If (parent)maxTurn -> (child)minTurn and player gets 2
    def lilFlopsies(self):
        return [ Flopsy(self.board, self.maxTurn,mv ) for mv in self.openSet ]
        '''
        from multiprocessing import Pool
        return [ Pool().apply( Flopsy, (self.board, self.maxTurn, mv) ) for mv in self.openSet ]
        '''    
def theMax(a,b):
    aInf = (type(a) == float)    
    bInf = (type(b) == float)
    if aInf and bInf:
        return a if ( a > b ) else b
    if aInf:
        return a if ( a > b.eval) else b
    if bInf:
        return b if ( b > a.eval ) else a
    return a if ( a.eval > b.eval ) else b

def theMin(a,b):
    aInf = (type(a) == float)    
    bInf = (type(b) == float)
    if aInf and bInf:
        return a if ( a < b) else b
    if aInf:
        return a if ( a < b.eval) else b
    if bInf:
        return b if ( b < a.eval ) else a
    return a if ( a.eval < b.eval ) else b

@Counter
def minMax(flopsy):
    if flopsy.isLeaf():
        return flopsy
    if flopsy.maxTurn:
        val = float('-inf')
    else:
        val = float('inf')
    for lil in flopsy.lilFlopsies():
        if flopsy.maxTurn:
            val = theMax( val, minMax(lil) )
        else:
            val = theMin( val, minMax(lil) )
    return val
