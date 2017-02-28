from __future__ import print_function
from constraint import *
from timeit import default_timer as timer
from itertools import combinations
from math import sqrt

# this program will create crossword patterns, but not fill it with words
# i.e. just patterns of zeros and ones for the black and white squares

# tests if a solution is fully connected i.e. can every point be reached from
# any random point. True if fullyconnected, false if disjoint parts.
# Could easily be made more efficient, but this works fine.
def isfullyconnected(solution):
    L = int(sqrt(len(solution)))
    # get list of all non-zero points
    plist = []
    for i in range(L):
        for j in range(L):
            if solution[i*L + j]: plist.append((i,j))
    
    # start top right corner, try to get to every other point
    reached = {plist[0]:1}
    rlen = len(reached)
    oldrlen = 0
    while rlen != oldrlen:
      temp = list(reached.keys())
      for i,j in temp:
        if (i+1,j) in plist: reached[(i+1,j)]=1
        if (i-1,j) in plist: reached[(i-1,j)]=1
        if (i,j+1) in plist: reached[(i,j+1)]=1
        if (i,j-1) in plist: reached[(i,j-1)]=1
      oldrlen = rlen
      rlen = len(reached)
    # if rlen is not eq number of all points, we couldn't reach some points
    if rlen < len(plist): return False
    return True    
    
from random import randint
    
def getPattern(sidelen=15,maxlen=9):
    problem = Problem()
    s = sidelen
    maxWordLen = maxlen
    problem.addVariables(list(range(s*s)), [0,1])
  
    # ensure there are no 2x2 blocks of ones or zeros
    def no4x4block(*x):
        if sum(x)==0: return False
        if sum(x)==len(x): return False
        else: return True

    for i in range(s-1):
        for j in range(s-1):
            problem.addConstraint(no4x4block,[i*s+j,(i*s+j)+1,(i*s+j)+s,(i*s+j)+s+1])
    
    #ensure matrix is symmetric  
    def eq(a,b):  
        return a==b

    for i in range(s):
        for j in range(s):
            problem.addConstraint(eq,[i*s+j,(s-i-1)*s+j])
            problem.addConstraint(eq,[i*s+j,i*s+(s-j-1)])
            problem.addConstraint(eq,[i*s+j,(s-i-1)*s+(s-j-1)])
       
    #ensure no words longer than maxWordLen
    def maxlen(*x):
        if sum(x) == len(x): return False
        else: return True

    seq = list(range(maxWordLen+1))
    for i in range(s - maxWordLen):
        for j in range(s):
            problem.addConstraint(maxlen,[(k+i)+j*s for k in seq])
            problem.addConstraint(maxlen,[(k+i)*s+j for k in seq])
    
    # no two letter words
    def no2letter(*x):
        if x == (0,1,1,0): return False
        else: return True
    
    seq = list(range(4))
    for i in range(s - 3):
        for j in range(s):
            problem.addConstraint(no2letter,[(k+i)+j*s for k in seq])
            problem.addConstraint(no2letter,[(k+i)*s+j for k in seq])

    # no two letter words around the edge either
    def no2letterEdge(*x):
        if x == (1,1,0): return False
        else: return True
    
    seq = list(range(4))
    for i in range(s):
        problem.addConstraint(no2letterEdge,[i,i+s,i+2*s])
        problem.addConstraint(no2letterEdge,[i*s,i*s+1,i*s+2])
        problem.addConstraint(no2letterEdge,[i*s+s-1,i*s+s-2,i*s+s-3])
        problem.addConstraint(no2letterEdge,[i+s*(s-1),i+s*(s-2),i+s*(s-3)])
    
    # no one letter squares
    def no1letter(*x):    
        if sum(x) == 0: return True
        if sum(x[1:]) == 0: return False
        return True
    
    seq = list(range(4))
    for i in range(s):
      for j in range(s):
        vals = [i*s+j]
        if i-1 >= 0: vals.append((i-1)*s+j) 
        if i+1 < s: vals.append((i+1)*s+j) 
        if j-1 >= 0: vals.append(i*s+(j-1)) 
        if j+1 < s: vals.append(i*s+(j+1)) 
        problem.addConstraint(no1letter,vals)
 
    # no more than three 0's in a row
    def nothreeblank(*x):
        if sum(x) == 0: return False
        return True
    
    seq = list(range(4))
    for i in range(s - 3):
        for j in range(s):
            problem.addConstraint(nothreeblank,[(k+i)+j*s for k in seq])
            problem.addConstraint(nothreeblank,[(k+i)*s+j for k in seq])
   
    for sol in problem.getSolutionIter():  
        if not isfullyconnected(sol): continue
        yield(sol)
    
from test_bin2hex import bin2hex
import sys
start = timer()
print(len(sys.argv))
if len(sys.argv)<2: sidelen = 11
else: sidelen = int(sys.argv[1])
print('using sidelen',sidelen)

f = open('pattern'+str(sidelen)+'.txt','w')
for count,sol in enumerate(getPattern(sidelen=sidelen,maxlen=8)):
    f.write(bin2hex(''.join([str(sol[a]) for a in range(sidelen*sidelen)]))+'\n')
    if count % 100 == 0: 
      print('count: '+str(count))
      print(bin2hex(''.join([str(sol[a]) for a in range(sidelen*sidelen)])))
      for i in range(sidelen):
        for j in range(sidelen): 
            if sol[i*sidelen+j]==1: print('.',end=' ')
            else: print('X',end=' ')
        print('')
      print('')
    #break
    
end = timer()    
print("solution time = " + str(end-start))