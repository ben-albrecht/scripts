#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function

import os

def main():
    """Recursively rename files from a renames.dat filemap, e.g.

        foo.txt bar.txt
    """


    filemap = {}

    with open('renames.dat', 'r') as handle:
        for line in handle.readlines():
            origname=line.split()[0]
            newname=line.split()[1]
            filemap[origname] = newname

    for root, dirs, files in os.walk('.'):
        if root == 'perf-report':
            continue
        for f in files:
            if f in filemap.keys():
                newfile = os.path.join(root, filemap[f])
                oldfile = os.path.join(root, f)
                print(f)
                if os.path.isfile(newfile):
                    print('data appended')
                    with open(newfile, 'r') as newhandle:
                        with open(oldfile, 'a') as oldhandle:
                            for line in newhandle.readlines()[1:]:
                                oldhandle.write(line)

                print(os.path.join(root, f), ' => ', os.path.join(root,filemap[f]))
                os.rename(oldfile, newfile)
                if os.path.isfile(oldfile):
                    print(oldfile, 'still exists..')
                    print('wtf?')


if __name__ == '__main__':
    main()
