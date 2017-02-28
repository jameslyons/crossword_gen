from math import sqrt
from test_bin2hex import bin2hex,hex2bin
import sys

def wordlocFromPattern(pattern):
    s = int(sqrt(len(pattern)))
    # extract the word positions from the pattern
    wordlocs = []
    hwordlocs = []
    vwordlocs = []
    for i in range(s):
        hword =  []
        vword = []
        for j in range(s):
            #if pattern[i*s + j] == 0: print(' ',end=' ')
            #else: print('X',end=' ')
            if pattern[i*s + j] == '1':
                hword.append(i*s + j)
            else:
                if len(hword) > 1: hwordlocs.append(hword)
                hword = []         
        
            if pattern[j*s + i] == '1':
                vword.append(j*s + i)
            else:
                if len(vword) > 1: vwordlocs.append(vword)
                vword = []
        
            if j == s-1:
                if len(vword) > 1 and vword not in vwordlocs: vwordlocs.append(vword)
                if len(hword) > 1 and hword not in hwordlocs: hwordlocs.append(hword)
            
        #print('')
    wordlocs.extend(vwordlocs)
    wordlocs.extend(hwordlocs) 
    return wordlocs
    
def lengthsFromPattern(p):
    words = wordlocFromPattern(p)
    lengths = [len(w) for w in words]
    return lengths
    
def numwhite(p):
    a = 0
    for i in p: 
        if i == '1': a+=1
    return a
    
def filterList(listname,k):
    f = open(listname)
    for line in f:
        pattern = hex2bin(line.strip())
        lengths = lengthsFromPattern(pattern)
        num3 = len([i for i in lengths if i==3])
        num4 = len([i for i in lengths if i==4])
        rat = numwhite(pattern)/(15*15)
        if rat > 0.70:
          if num3 > 0 and num3 <= 6: 
            if num4 > 0 and num4 <= 10: print(rat,num3,num4,line.strip())
    f.close()    
    
infilename = sys.argv[1]
k = int(sys.argv[2])
filterList(infilename,k)
    
    
    