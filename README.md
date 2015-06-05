# Various python / shell scripts created for my work.

## Frank Cluster
### submit
Generate PBS batch file for a Q-Chem job and submit it, based on CLI flags

### best_queue
Find best queue available for job specifications (WIP)
submit depends on best_queue (hence the best_queue.py sym link)

### multibatch
Create job array for multiple jobs and submit to a distributed queue (WIP)

### qs
Queue Status - quick summary of queue, and reveals empty queues

### pbsclean
Clean up the trash that pbs and submit script leaves everywhere

## General Use
### cpg
Cartesian Product Generator - Extension of Python's 
[itertools.product ](https://docs.python.org/3.3/library/itertools.html#itertools.product) for file text.
Primarily used to generate inputs with multiple changed paramaters (e.g. varying bond distances with varying basis sets)

### jabget
Convert .ris file format to .bib

### ipyr
IPython Remote - Instead of ssh'ing into a machine, 
access the remote machine through a hosted instance of Jupyter in browser.

### search
More code-specific grepping. I mostly use [The Silver Searcher](https://github.com/ggreer/the_silver_searcher) these days

### pdb
Fetch a pdb file from protein database, given a pdb index

## Q-Chem
### errors
Quick and dirty error report for Q-Chem jobs, searches for common errors

## Personal
### eg
Quickly navigate topics in my eg repository

### ref
Quickly navigate topics in my ref repository

### gitrep
Manage multiple git repositories at once


## Undocumented
dirtags.sh
geomopt
plotvfile
qchemall
qcmake
qcmake.py
qctags
qdelr
qfold
qgrep
rextract
rmsd
runall
search
submit
submitbatch
submitqchemall
zmat
