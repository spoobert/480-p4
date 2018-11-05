from itertools import product
import collections
from perm import perm 
herdSize = 0
#getCount = None
def Counter(f):
    global getCount
    n = 0
    getCount = lambda: n
    def inner(*args, **kwargs):
        nonlocal n
        n += 1
        return f(*args, **kwargs)
    return inner

# Flopsy represents the next chosen move in the game
# 'root' Flopsy is the initial game state
# Flopsy is mad at Mommy...Flopsy:= playerNot(Mommy.player) ; maxTurnNot(Mommy.maxTurn)
class abFlopsy():
    def __init__(self, board, maxT=True, mv='root', d=0):
        global herdSize 
        herdSize += 1
        self.move = mv
        self.maxTurn = False if maxT else True
        self.board = [ [p for p in line] for line in board ]
        if mv != 'root':
            self.board[mv[0]][mv[1]] = 1 if self.maxTurn else 2
        #swap i,j -> j,i to make row major order
        self.openSet = [ (i,j) for j,i in product( range(4), range(4)) if self.board[i][j] == 0 ]
        self.p1Count = sum( map(self.findPossiblePOne,perm) )
        self.p2Count = sum( map(self.findPossiblePTwo,perm) ) 
        self.p1Won = True if [ p for p in map(self.mapFindWinner,perm) if p == 1] else False
        self.p2Won = True if [ p for p in map(self.mapFindWinner,perm) if p == 2] else False
        self.eval = self.staticEval()
        self.depth = d 
    
    def __repr__(self):
        return str(self.board[0])+ '\n'  + str(self.board[1]) + '\n' + str(self.board[2])+'\n' + str(self.board[3]) + '\n' +' depth ' + str(self.depth) +' mv: '+str(self.move)
        
    def isLeaf(self):
        
        if self.p1Won:
            #print('P1 wins --> leaf')
            #print(self)
            return True
        if self.p2Won:
            #print('P2 wins --> leaf')
            #print(self)
            return True
        if self.openSet == []:
            #print('openSet empty --> leaf')
            #print(self)
            return True
        
        #if self.depth == 6:
        #   return True
        #return False 

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
        return [ abFlopsy(self.board, self.maxTurn,mv, self.depth + 1 ) for mv in self.openSet ]
        
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

def ltEt(a,b):
    try:
        #aInf = (type(a) == float) or (type(a) == int)    
        #bInf = (type(b) == float) or (type(b) == int)
        aInf = (type(a) == float)    
        bInf = (type(b) == float)
        #if(type(a) == int):
        #    if(bInf or (type(b) == int)):
        #        return a if (a <= b) else b
        #    return a if (a <= b.eval) else b
        #if(type(b) == int):
        #    if(aInf or type(a) == int):
        #        return a if (a <= b) else b
        #    return a if (a.eval <= b) else b
        if aInf and bInf:
            return a if ( a <= b) else b
        if aInf:
            return a if ( a <= b.eval) else b
        if bInf:
            return b if ( b <= a.eval ) else a
        return a if ( a.eval <= b.eval ) else b
    except:
        #print("error: ", type(a), ' ', type(b))
        #exit(1)
        '''
        if(type(a) == int):
            return a
        if(type(b) == int):
            return b
        '''
        if(type(a) == int):
            if(bInf or (type(b) == int)):
                return a if (a <= b) else b
            return a if (a <= b.eval) else b
        if(type(b) == int):
            if(aInf or type(a) == int):
                return a if (a <= b) else b
            return a if (a.eval <= b) else b

#TODO Check for Valid board
@Counter
def abMiniMax(flopsy,alpha=float('-inf'),beta=float('inf')):
    #print(flopsy)    
    if flopsy.isLeaf():
        return flopsy
    if flopsy.maxTurn:
        #res = alpha
        res = float("-inf")
        for lil in flopsy.lilFlopsies():
            #val = abMiniMax(lil,res,beta)
            val = abMiniMax(lil,alpha,flopsy.eval)
            res = theMax(res, val) 
            if ltEt(beta,res):
                return res
    else:
        #res = beta
        res = float("inf")
        for lil in flopsy.lilFlopsies():
            #val = abMiniMax(lil, alpha, res)
            val = abMiniMax(lil, flopsy.eval, beta)
            res = theMin( res, val )  
            if ltEt(res, alpha):
                return res
    return res
