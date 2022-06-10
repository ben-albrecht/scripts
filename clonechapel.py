#!/usr/bin/env python

from __future__ import print_function

import os
import shlex
import subprocess
import sys
import re

from fire import Fire


def main():
    destination = next_number()
    repository = 'git@github.com:ben-albrecht/chapel.git'

    print('Cloning into directory: {1}\nOK? [y/N]?'.format(repository, destination))
    response = raw_input()
    if response != 'y':
        print('Aborting')
        sys.exit()

    git_clone(repository, destination)
    add_remote(destination)
    add_modulefile(destination)


def next_number():
    """Get next number in directories named after range: 1.."""
    p = subprocess.check_output('ls')
    files = p.split()
    regex = re.compile('^\d+$')
    copies = filter(regex.match, files)
    numbers = filter(int, copies)
    return int(max(numbers))+1


def git_clone(repo, dest):
    """Clone repository to destination"""
    cmd = 'git clone {0} {1}'.format(repo, dest)
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, bufsize=1)
    for line in iter(p.stdout.readline, b''):
        print(line, end='')
    p.stdout.close()
    p.wait()

def add_remote(dest):
    """Add remote upstream"""
    os.chdir(str(dest))
    cmd = 'git remote add upstream git@github.com:chapel-lang/chapel.git'
    p = subprocess.Popen(shlex.split(cmd))
    p.wait()


def add_modulefile(destination):
    """Get the module path and add a chapel module for the new number"""
    # TODO: Try 'module show chapel' ?
    # Temporarily hard-coded
    modulepath = '/Users/balbrecht/repos/modules/mbp-balbrecht/chapel'
    os.chdir(modulepath)
    os.symlink('1', destination)



if __name__ == '__main__':
    Fire(main)
