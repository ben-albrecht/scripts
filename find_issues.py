#!/usr/bin/env python3

"""Find and print a list of GitHub issues found recursively within a given path.

If PyGithub is available, prints the status of each issue.

Requires python 3 and PyGithub package
"""

import argparse
import os
import re
import shlex
import subprocess

try:
    from github import Github
    github_available = True
except ImportError:
    print('Warning: Unable to import PyGithub, skipping issue validation')
    github_available = False


argparser = argparse.ArgumentParser(description=__doc__)
argparser.add_argument('path',
                        help='path to be searched recursively for issue numbers')
argparser.add_argument('--lines',  action='store_true', default=False,
                        help='Print lines containing issues for context')
argparser.add_argument('--false_positives', action='store_true',
                        default=False, help='Print issues marked as false positives')
argparser.add_argument('--quiet', action='store_true', default=False,
                        help='Silence parsing warnings')
argparser.add_argument('--no_status', action='store_true', default=False,
                        help='Do not check issue status on Github')
argparser.add_argument('--blame', action='store_true', default=False,
                        help='Perform a git blame on the lines containing issues')

# TODO: Args for how to print issue status
FLAGS = argparser.parse_args()

check_status = not FLAGS.no_status and github_available
if check_status:
    g = Github()
    repo = g.get_repo('chapel-lang/chapel')

def main():
    path = FLAGS.path

    # Parse issue numbers
    issues = parse_issues(path)

    return


def print_issue(issue):
    (f, line, issue_number, fp, line_number) = issue

    if fp and not FLAGS.false_positives:
        return


    msg = f'{f} : #{issue_number}'

    if fp:
        msg += ' (false positive)'

    # Check status of each issue
    if check_status:
        try:
            issue = repo.get_issue(issue_number)
            if issue.pull_request is None:
                status = issue.state
            else:
                status = f'(PR - {issue.state})'
        except:
            status = '(error accessing github)'

        msg += f' ({status})'


    print(msg)
    if FLAGS.lines:
        print(line)

    if FLAGS.blame:
        try:
            cmd = f'git blame -L {line_number},{line_number} {f}'
            print(cmd)
            output = subprocess.check_output(shlex.split(cmd))
        except:
            print('Error performing git blame')
            raise
        print(output.decode())



def parse_issues(path):

    issues = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            fullpath = os.path.join(dirpath, filename)
            # If the try fails, we want this to still be empty
            found_issues = []
            try:
                found_issues = grep_issue_numbers(fullpath)
            except UnicodeDecodeError:
                if not FLAGS.quiet:
                    print(f'Error parsing {filename}')
            for issue in found_issues:
                issues.append(issue)
                print_issue(issue)

    return issues

# (filename, line, issue_number, false-positive)

def grep_issue_numbers(filename):
    issue_pattern = re.compile(r'#[0-9]+\b')
    issues = []
    with open(filename) as handle:
        line_number = 0
        for line in handle.readlines():
            line_number += 1
            matches = re.findall(issue_pattern, line)
            if matches:
                for match in matches:
                    issue_number = int(match[1:])
                    false_positive = detect_false_positives(line, issue_number)
                    data = (filename, line, issue_number, false_positive, line_number)
                    issues.append(data)
    return issues



def detect_false_positives(line, issue_number):
    """Some heuristics for determining if regex was actually a reference"""

    # Ignore count operator instances
    if '..' in line:
        return True

    # First issue starts at 4945
    if issue_number < 4945:
        return True


    return False




if __name__ == '__main__':
    main()


