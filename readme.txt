readme

-generate patterns with cw_genpatterns.py
- this was done into patterns15.txt
- some of the patterns aren't good, we have filtered the good ones using cw_filterpattern.py 
  into pattern15_6.txt
- some of the previous patterns are mostly empty, kept only >70% white in pattern15_7.txt
- we then run cw_fill2.py, it pulls a random pattern from pattern15_7 and fills it with words,
  outputing it to temp.txt using
NUMITER=10; echo -n > temp.txt; i=0; while [ $i -lt $NUMITER ]; do echo -n $i'-'; timeout 10 ../../Downloads/pypy2-v5
.6.0-win32/pypy2-v5.6.0-win32/pypy cw_fill2.py >> temp.txt; if [ $? -eq 124 ] ; then echo 'timed out'; else echo 'done'
; let "i=i+1"; fi done

- run cw_typeset2.py, it takes temp.txt and typesets each of the solutions in temp into auto0.tex -> autoN.tex
- use latex to compile crossword2.tex to get final document