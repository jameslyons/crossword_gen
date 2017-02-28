#Generating codeword puzzles with python

Basically this code first generates large numbers of crossword patterns, which are then filtered leaving us with a few that have good properties. In this case pattern15_7.txt holds the representations of a few patterns that I consider good. More patterns would be advantageous, it will be done if I ever get around to it.

Once the patterns are generated, cw_fill2.py uses the wordlist in game2.txt to populate the crossword. These completed crosswords are output to a file that is read by cw_typeset2.py, which outputs a series of tex files which get `include`d into crossword2.tex. It is then simply a matter of compiling the tex file to get a PDF of pretty crossword/codeword puzzles.

If you don't want to generate your own patterns, skip the first 3 steps.

- generate patterns with `python cw_genpatterns.py > patterns15.txt`. I left this for a few days, it takes a long time to find good crossword patterns. 
- some of the patterns aren't good, we have filtered the good ones using `python cw_filterpattern.py > pattern15_6.txt`. 
- some of the previous patterns are mostly empty, kept only >70% white in pattern15_7.txt
- we then run `python cw_fill2.py`, it pulls a random pattern from pattern15_7 and fills it with words,
  outputing it to temp.txt using:
  
  ```bash
  NUMITER=10; echo -n > temp.txt; i=0; while [ $i -lt $NUMITER ]; do echo -n $i'-'; timeout 10 ../../Downloads/pypy2-v5.6.0-win32/pypy2-v5.6.0-win32/pypy cw_fill2.py >> temp.txt; if [ $? -eq 124 ] ; then echo 'timed out'; else echo 'done'; let "i=i+1"; fi done
  ```
  
- run `python cw_typeset2.py`, it takes temp.txt and typesets each of the solutions in temp into auto0.tex -> autoN.tex
- use latex to compile crossword2.tex to get final document
