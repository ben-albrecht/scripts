#!/usr/bin/env python
# encoding: utf-8

from subprocess import Popen, PIPE
import sys
import shlex


def run_cmd(cmd, verbose=False):
    if verbose:
        print(command)
    process = Popen(shlex.split(command), stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if verbose:
        print(stdout)
        print(stderr)


def git_delete_remote(branch):
    basecommand = 'git push origin --delete '
    command = basecommand + branch
    run_cmd(command, verbose=True)

def git_delete_remote(branch):
    basecommand = 'git branch -d '
    command = basecommand + branch
    run_cmd(command, verbose=True)



# TODO -- add this to script: (except just pipe output to a list)
#    git branch --merged | egrep -v "(^\*|master|dev)" | > del.txt

def main():
    with open('del.txt', 'r') as deletesfile:
        for branch in [b.strip() for b in deletesfile.readlines()]:
            git_delete_local(branch)
            git_delete_remote(branch)



if __name__ == '__main__':
    main()
