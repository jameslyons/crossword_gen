from __future__ import print_function
from constraint import *
from timeit import default_timer as timer
from itertools import combinations
from math import sqrt,floor
from test_bin2hex import hex2bin
import sys

from random import randint

''' to run from pypy
..\..\Downloads\pypy2-v5.6.0-win32\pypy2-v5.6.0-win32\pypy cw_fill.py 34832F232983h
'''
# this program will take a crossword pattern and try to fill it with words

# we want to choose a random line in pattern file without iterating through everything
patternfile = open('pattern15_7.txt')
'''linelen = 0
for line in patternfile: 
    linelen = len(line) # includes newline
    break
patternfile.seek(0,2)
flen = patternfile.tell()
nlines = floor(flen/linelen)    

roffset = randint(0,nlines-2)
patternfile.seek(roffset*linelen)
patternfile.readline()
pattern = patternfile.readline().strip()
pattern = pattern.split()[2]
'''

patterns = patternfile.readlines()
roffset = randint(0,len(patterns)-1)
pattern = patterns[roffset].split()[3]

patternfile.close()

pattern = hex2bin(pattern) 
pattern = [int(i) for i in pattern]


s = int(sqrt(len(pattern)))

# extract the word positions from the pattern
wordlocs = []
hwordlocs = []
vwordlocs = []
for i in range(s):
    hword =  []
    vword = []
    for j in range(s):
        if pattern[i*s + j] == 1:
            hword.append(i*s + j)
        else:
            if len(hword) > 1: hwordlocs.append(hword)
            hword = []         
        
        if pattern[j*s + i] == 1:
            vword.append(j*s + i)
        else:
            if len(vword) > 1: vwordlocs.append(vword)
            vword = []
        
        if j == s-1:
            if len(vword) > 1 and vword not in vwordlocs: vwordlocs.append(vword)
            if len(hword) > 1 and hword not in hwordlocs: hwordlocs.append(hword)
wordlocs.extend(vwordlocs)
wordlocs.extend(hwordlocs)

wordlist = []
f = open("game2.txt")
for line in f:
    w = line.split()[0].lower()
    wordlist.append(w)

wordlen = []
olen = 0
for c,word in enumerate(wordlist):
    if olen < len(word):
        wordlen.append(c)
    olen = len(word)

problem = Problem()
from random import shuffle

for c,w in enumerate(wordlocs):
    L = len(w)-3
    r = list(range(wordlen[L],wordlen[L+1]))
    shuffle(r)
    problem.addVariables([c], list(r))

problem.addConstraint(AllDifferentConstraint())

def eq(a,b):
    def temp(c1,c2):
        word1 = wordlist[c1]
        word2 = wordlist[c2]
        if word1[a]==word2[b]: return True
        return False
    return temp
        
for c1,word1 in enumerate(wordlocs):
    for c2,word2 in enumerate(wordlocs):
        if word1==word2: continue
        intsc = list(set(word1).intersection(set(word2)))
        if len(intsc) > 0:
            a = word1.index(intsc[0])
            b = word2.index(intsc[0])
            problem.addConstraint(eq(a,b),[c1,c2])    

# pretty print the output
for count,a in enumerate(problem.getSolutionIter()):  
    sol = ['.' for i in range(s*s)]
    for key,val in a.iteritems():
        for c,char in enumerate(wordlist[val]):
            sol[wordlocs[key][c]] = char      
    print(''.join([str(sol[i]) for i in range(s*s)]))
    break
