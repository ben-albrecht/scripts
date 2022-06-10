#!/usr/bin/env python3
# encoding: utf-8
"""
Map .graph graphtitle -> .chpl tests

Cases not covered:
    - finding .dat files lists in .perfkeys
    - covering repeat-files: field

"""

import os

def parsegraphs(graphfiles='GRAPHFILES'):
    graphs = []
    with open(graphfiles, 'r') as handle:
        for line in handle.readlines():
            if '#' != line.lstrip()[0]:
                graphs.append(line.strip())
    return graphs

def parsegraph(graphfile):
    datfiles = []
    # {.graph : [.dat files]} map
    graphdatmap = {}

    with open(graphfile, 'r') as handle:
        for line in [l.strip() for l in handle.readlines()]:
            # Next grouping
            if len(line) == 0:
                graphdatmap[graphtitle] = datfiles
                datfiles = []
                graphtitle = ''
            # datfiles
            if line.startswith('files'):
                datfiles.extend(line.split(':')[1].strip().split(','))
            # graphtitle
            elif line.startswith('graphtitle'):
                graphtitle = line.split(':')[1].strip()
        # Clean up
        if graphtitle not in graphdatmap.keys():
            graphdatmap[graphtitle] = datfiles
    return graphdatmap


def grep(s, f):
    """Return true if s is found in file f, else false"""
    if not os.path.exists(f):
        return False
    with open(f, 'r') as handle:
        for line in handle.readlines():
            if s in line:
                return True
    return False


def getgraphchplmap(graphtitle, datfiles, graphfile):
    dirname = os.path.dirname(graphfile)
    chplfiles = set()
    if not dirname:
        dirname = '.'
    for dat in datfiles:
        chplfile = ''
        datbasename = os.path.splitext(dat)[0].strip()
        ls = os.listdir(dirname)
        perfoptsfiles = [l for l in ls if l.endswith('.perfexecopts') or l.endswith('.perfcompopts')]
        optsfiles = [l for l in ls if l.endswith('.execopts') or l.endswith('.compopts')]
        for perfoptsfile in perfoptsfiles:
            if grep('#', os.path.join(dirname, perfoptsfile)):
                basename = os.path.splitext(perfoptsfile)[0].strip()
                chplfile = os.path.join(dirname, basename+'.chpl')
                chplfiles.add(chplfile)
                break
        if not chplfile:
            for optsfile in optsfiles:
                if grep('#', os.path.join(dirname, optsfile)):
                    basename = os.path.splitext(optsfile)[0].strip()
                    chplfile = os.path.join(dirname, basename+'.chpl')
                    chplfiles.add(chplfile)
                    break
        if not chplfile:
            basename = os.path.splitext(dat)[0].strip()
            chplfile = os.path.join(dirname, basename+'.chpl')
            chplfiles.add(chplfile)

    return chplfiles


def main():

    graphs = parsegraphs()
    graphchplmap = {}
    for g in graphs:
        graphdatmap = parsegraph(g)
        for graphtitle, datfiles in graphdatmap.items():
            graphchplmap[graphtitle] = getgraphchplmap(graphtitle, datfiles, g)

    for graphtitle, chplfiles in graphchplmap.items():
        print(graphtitle)
        for chplfile in chplfiles:
            print('  ', chplfile)

if __name__ == '__main__':
    main()
