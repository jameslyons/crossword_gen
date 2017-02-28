from math import sqrt

def getwords(solution):
  s = int(sqrt(len(solution)))
  # extract the word positions from the pattern
  wordlocs = []
  wordvals = []
  for i in range(s):
    hword,hloc =  [],[]
    vword,vloc = [],[]
    for j in range(s):
        if solution[i*s + j] != '.':
            hword.append(solution[i*s + j])
            hloc.append(i*s + j)            
        else:
            if len(hword) > 1: 
                wordvals.append(hword)
                wordlocs.append(hloc)
            hword,hloc = [],[]         
        
        if solution[j*s + i] != '.':
            vword.append(solution[j*s + i])
            vloc.append(j*s + i)            
        else:
            if len(vword) > 1: 
                wordvals.append(vword)
                wordlocs.append(vloc)
            vword,vloc = [],[]
        
        if j == s-1:
            if len(vword) > 1 and vword not in wordvals: 
                wordvals.append(vword)
                wordlocs.append(vloc)
            if len(hword) > 1 and hword not in wordvals:
                wordvals.append(hword)
                wordlocs.append(hloc)
  return wordvals,wordlocs

def frequencies(solution):
    freq = {}
    for i in range(len(solution)):
        if solution[i] == '.': continue
        if solution[i] in freq: freq[solution[i]] += 1
        else: freq[solution[i]] = 1
    return freq

def bestword(solution):
    words,locs = getwords(solution)
    freqs = frequencies(solution)
    maxfreq = 0
    maxword = ''
    for i in range(len(words)):
        if len(set(words[i])) != 3: continue
        if len(words[i]) != 3: continue
        totfreq = sum([freqs[i] for i in words[i]])/len(words[i])
        if totfreq > maxfreq:
            maxfreq = totfreq
            maxword = locs[i]
    return maxword
    
from random import shuffle
    
def typeset(solution,outfname='solution.tex'):
    f = open(outfname,'w')
    vars = list(range(1,27))
    shuffle(vars)
    map = dict(zip('abcdefghijklmnopqrstuvwxyz',vars))
    def a2i(a): return map[a.lower()]
    unmap = dict(zip(vars,'abcdefghijklmnopqrstuvwxyz'.upper()))
    def i2a(a): return unmap[i]
    # choose a three letter word with some common letters
    hint = bestword(solution)
    
    
    L = int(sqrt(len(solution)))

    #print(r'\documentclass{article}')
    #print(r'\usepackage[unboxed]{cwpuzzle}')
    #print(r'\begin{document}')
    #print(r'\renewcommand{\PuzzleBlackBox}{\framebox(.75,.75){\framebox(.5,.5){\framebox(.25,.25){}}}}')
    
    f.write('\\begin{minipage}{.25\\textwidth}\n')
    hintletters = [solution[i].upper() for i in hint]
    f.write('\\begin{Puzzle}{4}{13}\n')
    for n,char in enumerate('ABCDEFGHIJKLM'):
        f.write('\\Frame{0}{'+str(13-n-1)+'}{1}{1}{'+str(n+1)+'}\n')
        f.write('\\Frame{2}{'+str(13-n-1)+'}{1}{1}{'+str(n+14)+'}\n')

    a = 'ABCDEFGHIJKLM'
    b = 'NOPQRSTUVWXYZ'
    for i,c in enumerate(a):
        f.write('|A|[]')
        nums = [a2i(solution[k]) for k in hint]
        #print(nums)
        if i+1 in nums: f.write('[rSf]'+hintletters[nums.index(i+1)])
        else: f.write('[r]A')        
        f.write('|A|[]')
        if i+14 in nums: f.write('[Sf]'+hintletters[nums.index(i+14)])
        else: f.write('A')
        f.write('|.\n')
    f.write('\\end{Puzzle}\n')
    f.write('\\end{minipage}%\n')

    f.write('\\begin{minipage}{.6\\textwidth}\n')
    
    f.write('\\begin{Puzzle}{'+str(L)+'}{'+str(L)+'}\n')

    for i in range(L):
      for j in range(L):
        f.write('|')

        if solution[i*L+j]=='.': f.write('* ')
        else:
            if i*L+j in hint: f.write('['+str(a2i(solution[i*L+j]))+'][Sf]'+solution[i*L+j].upper())        
            else: f.write('['+str(a2i(solution[i*L+j]))+']'+solution[i*L+j].upper())
      f.write('|.\n')
    f.write('\\end{Puzzle}\n')
    f.write('\\end{minipage}%\n')
    f.write('\\begin{minipage}{.2\\textwidth}\n')
    hintletters = [solution[i].upper() for i in hint]
    f.write('\\begin{Puzzle}{2}{13}\n')

    a = 'ABCDEFGHIJKLM'
    b = 'NOPQRSTUVWXYZ'
    for i,c in enumerate(a):
        f.write('|[][S]'+a[i]+'|[][S]'+b[i]+'|.\n')
    f.write('\\end{Puzzle}\n')
    f.write('\\end{minipage}%\n')

    
import sys

#typeset(sys.argv[1],outfname=sys.argv[2])

outfilename = 'sol'
solfile = open('temp.txt')
for c,sol in enumerate(solfile):
    typeset(sol,outfname='auto'+str(c)+'.tex')
