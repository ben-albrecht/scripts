#!/usr/bin/env python3
# encoding: utf-8

import os
import shlex
import subprocess
import sys

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    try:
        os.chdir(sys.argv[1])
    except:
        print('Directory not found')
        print_help()
        sys.exit(2)

    branches = subprocess.check_output(shlex.split("git branch --merged")).decode()
    branches = branches.split()
    branches = [b for b in branches if '*' not in b and 'master' not in b]

    for branch in branches:
        print(branch)
        delete_cmd = 'git push --delete origin {0}'.format(branch)
        prune_cmd = 'git branch -dr {0}'.format(branch)
        subprocess.call(shlex.split(delete_cmd))
        subprocess.call(shlex.split(prune_cmd))


def print_help():
    print()
    print('Usage:')
    print('./deletemerged.py <repository>')

if __name__ == '__main__':
    main()
