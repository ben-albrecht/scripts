#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
import os
import sys


def main():
    chpl_home = os.getenv('CHPL_HOME')

    if not chpl_home:
        sys.exit(1)

    testdir = os.path.join(chpl_home, 'test', os.path.relpath(os.getcwd(), chpl_home))

    if not testdir:
        sys.exit(1)

    return testdir



if __name__ == '__main__':
    print(main())
