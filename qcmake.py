#!/usr/bin/env python
from os import environ, chdir
import sys

from argparse import ArgumentParser, RawTextHelpFormatter
import subprocess
import shlex



def get_arguments(args=None):
    """
    Get arguments from command line
    :args: Arguments, if predefined
    :returns: Opts, the arguments parsed
    """
    parser = ArgumentParser(prog='qcmake',
                            usage='%(prog)s [options] ',
                            description="""
===================================================
Wrapper script for make Q-Chem.
Running qcmake with no options will just build Q-Chem with the existing options
if it has already been configured
===================================================
    Compilers (choose one):
 * gcc         -- GNU compilers (gcc/g++/gfortran)
 * intel       -- Intel compilers (icc/icpc/ifort)
 * mingw32     -- MinGW32 GNU compilers (mingw32-gcc/mingw32-g++/mingw32-gfortran)
 * msys        -- MSYS GNU compilers (gcc/g++/gfortran)
 * open64      -- Open64 compilers (opencc/openCC/openf90)
 * ibm         -- IBM XL compilers (xlc/xlc++/xlf)
 * pgi         -- Portland Group compilers (pgcc/pgCC/pgf90)
 * cray        -- Cray compilers (cc/CC/ftn), includes MPI support

Build type (optional):
 * nointracule -- Compile with NO_INTRACULE
                  (Saves time on libint compilation)
 * nonewpath2  -- Compile with NO_NEW_PATH2
                  (Saves time on libint/new-hgp-codes)
 * nolibdftn   -- Compile without libdftn
 * nobigdft    -- Turns off large DFT codes (>1.5MB)
                  (Saves time on libdftn compilation)
 * nolibintok  -- Compile without libintok
 * nomgc       -- Compile without MGC
                  (Saves time on ccman compilation)
 * noccman2    -- Compile without ccman2
 * nodmrg      -- Compile without the DMRG module
                  (Use in case of problems with Boost)
 * noopt1      -- Use with 8 Gb of RAM or less
 * noopt2      -- Use with 4 Gb of RAM or less
 * debug       -- Quick build with debugging info
 * release     -- Slow build with optimizations
 * distrib     -- Optimized build with license checks
 * relwdeb     -- Optimized build with debugging info
 * static      -- Build a statically linked executable
 * timings     -- Include timings
 * verbose     -- Produce verbose logs for debugging

Linear algebra libraries (choose one):
 * mkl         -- Intel MKL (specify $MKLROOT)
 * acml        -- AMD ACML (specify $ACMLROOT)
 * essl        -- IBM ESSL
 * atlas       -- ATLAS ($QC_EXT_LIBS/atlas)
 * openblas    -- OpenBLAS ($QC_EXT_LIBS/OpenBLAS)

OpenMP/MPI (optional):
 * openmp      -- Enables OpenMP
 * openmpi     -- Enables Open MPI as MPI backend
                  (Must be under $QC_EXT_LIBS/openmpi)
 * mpich       -- Enables MPICH as MPI backend
                  (Must be under $QC_EXT_LIBS/mpich)
 * mpich2      -- Enables MPICH2 as MPI backend
                  (Must be under $QC_EXT_LIBS/mpich2)

Accelerators (optional):
 * cuda        -- Enables CUDA support
                            """,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('--compiler', choices=['gcc', 'intel'],
                        default=None, help='Compiler')
    parser.add_argument('--math',
                        choices=['mkl', 'openblas', 'acml', 'atlas', 'essl'],
                        help='Math Library')
    parser.add_argument('--configure', nargs='+',
                        default=None, help='Additional configure flags')
    parser.add_argument('--optimization',
                        default=None, help='Optimization level (0-3)')

    opts = parser.parse_args(args)
    return opts


def run(commands, verbose=True):
    """Wrapper for running/printing output"""
    out = subprocess.Popen(shlex.split(commands),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
    if verbose:
        for line in iter(out.stdout.readline, b''):
            print(">>> " + line.rstrip())
    return out


def link(QC):
    """Link executable and tests"""
    run('mkdir '+QC+'/exe', verbose=False)
    run('ln -fs '+QC+'/build/qcprog.exe          '+QC+'/exe/qcprog.exe')
    run('ln -fs '+QC+'/build/diffParseAlone.exe '+QC+'/util/cronutil/diffParseAlone.exe')
    run('ln -fs '+QC+'/build/mergeLines.exe     '+QC+'/util/cronutil/mergeLines.exe')


def qc():
    """Check for and return $QC environment variable"""
    QC = environ.get('QC')
    if not QC:
        print('$QC is not set!')
        sys.exit(1)
    return QC


def main(compiler=None, math=None, configure=None, optimization=None):

    QC = qc()
    QCBUILD = QC+'/build'

    if (compiler or math or configure or optimization):
        chdir(QC)

        #./configure intel nointracule nomgc noopt2 nolibdftn nonewpath2 release mkl
        configurecmd = ['./configure', compiler, math]
        configurecmd.extend(configure)
        configurecmd = ' '.join(configurecmd)

        run(configurecmd)

        opt2 = "sed -i -e 's/-O2/-O"+str(optimization)+"/g' "+QCBUILD+"/CMakeCache.txt"
        opt3 = "sed -i -e 's/-O3/-O"+str(optimization)+"/g' "+QCBUILD+"/CMakeCache.txt"

        run(opt2)
        run(opt3)

    print('cd ' + QCBUILD)
    chdir(QCBUILD)
    run('make -j4')
    link(QC)


if __name__ == '__main__':
    opts = get_arguments()
    main(compiler=opts.compiler,
         math=opts.math,
         configure=opts.configure,
         optimization=opts.optimization)
