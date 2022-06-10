#!/usr/bin/env python3
# encoding: utf-8

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import os
import subprocess


"""
Script to bisect performance tests

Good performance = exit 0
Bad performance = exit 1
Failure = exit 2
"""
def main():
    args = get_arguments()
    subprocess


#
# Notes:
# Rebuild the compiler
#   make -j 4
# Set CHPL_TEST_PERF_DIR
# Wipe CHPL_TEST_PERF_DIR
# Run the performance test 'positional arg'
#   start_test --performance --num-trials 5
# # Extract average of 'perfkey' column from 'datfile'
#



def get_arguments(args=None):
    """
    Get arguments from command line
    :args: arguments, if predefined
    :returns: arguments parsed
    """
    parser = ArgumentParser(prog='progname',
                            usage='%(prog)s  usage [options] ',
                            description=''' %(prog)s  description''',
                            formatter_class=ArgumentDefaultsHelpFormatter
                            )
    parser.add_argument('chplfile', help='Test to run')
    parser.add_argument('datfile', help='datfile to check')
    parser.add_argument('perfkey', help='Column of datfile to check')
    opts = parser.parse_args(args)
    return opts


if __name__ == '__main__':
    if not os.getenv('CHPL_HOME'):
        print('CHPL_HOME not set!')
        exit(255)
    main()
