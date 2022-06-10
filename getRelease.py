#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import os
import shutil
import shlex
import subprocess
import sys

import fire


def wget(URL):
    cmd = 'wget {0}'.format(URL)
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, bufsize=1)
    for line in iter(p.stdout.readline, b''):
        print(line, end='')
    p.stdout.close()
    p.wait()

def unpack(targz):
    cmd = 'tar -xzf {0}'.format(targz)
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, bufsize=1)
    for line in iter(p.stdout.readline, b''):
        print(line, end='')
    p.stdout.close()
    p.wait()
    os.remove(targz)


def main(version):
    """Download release version number, unpack tarball, overwriting
    any existing copy of that version number"""

    if version in os.listdir('.'):
        print('{0} already exists.\nOverwrite? [y/N]'.format(version))
        response = raw_input()
        if response != 'y':
            print('Aborting')
            sys.exit()

        print('Removing {0}'.format(version))
        shutil.rmtree(version)


    URL = 'https://github.com/chapel-lang/chapel/releases/download/{0}/chapel-{0}.tar.gz'.format(version)
    wget(URL)

    targz = 'chapel-{0}.tar.gz'.format(version)
    unpack(targz)

    release = 'chapel-{0}'.format(version)
    os.rename(release, version)


if __name__ == '__main__':
    fire.Fire(main)
