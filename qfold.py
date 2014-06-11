from subprocess import check_call, check_output, CalledProcessError
import math
import re
import os


def get_basis(handle):
    """ Find NBasis using regex in file"""
    return 36
    #lines = handle.readline()
    #num = 0
    #while num < len(lines):
    #    line = lines[num]
    #    if "basis functions" in line:
    #        print "found"
    #        m = re.search('basis (.+?) functions', line)
    #        return 22
    #        #if m:
    #            #return m.group(1)
    #    else:
    #        num += 1


def matlines(NBasis, cols):
    """ Calculate number of lines in a matrix  depending on NBasis """
    return int((math.ceil(float(NBasis)/cols))*(NBasis+1))
      



# main function
# future - check for scf_print > 2, and ~/.vim/view
# fname = arg.parse()
fname = 'emb111.out'


starts = []
ends = []

with open(fname, 'r') as handle:

    NBasis = get_basis(handle)
    print "NBasis = ", NBasis

    matsize6 = matlines(NBasis,6.0)
    matsize4 = matlines(NBasis,4.0)
    
    print "matsize6 = ", matsize6
    print "matsize4 = ", matsize4

    repattern = 'jPA'

    regex_pattern6 = re.compile(r'\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)')
    regex_pattern4 = re.compile(r'\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)')

    lines = handle.readlines()
    
    #for num, line in enumerate(lines):
    num = 0
    while num < len(lines):
        line = lines[num]

        # Managers
        if "Welcome to Q-Chem" in line:
            starts.append(num)
            found = False
            while not found:
                num += 1
                if "User input:" in lines[num]:
                    found = True
                    ends.append(num+1)
                    line = lines[num]

        if "Job number = 20" in line:
            starts.append(num)
            found = False
            while not found:
                num += 1
                if "Total DFTman time = " in lines[num]:
                    found = True
                    ends.append(num+1)
                    line = lines[num]

        if "Setting up Fragment 1-in-2 Calculation" in line:
            starts.append(num)
            found = False
            while not found:
                num += 1
                if "Embed Summary" in lines[num]:
                    found = True
                    ends.append(num-2)
                    line = lines[num]

        if "Calling Get_Boys in C++" in line:
            starts.append(num)
            found = False
            while not found:
                num += 1
                if "EXECUTING ORTHO_FUNC DESTRUCTOR" in lines[num]:
                    found = True
                    ends.append(num+1)
                    line = lines[num]

        if "contents of the context" in line:
            starts.append(num)
            found = False
            while not found:
                num += 1
                if "Total ccman2 time" in lines[num]:
                    found = True
                    ends.append(num+1)
                    line = lines[num]


        if "ccman2 parameters structure" in line:
            starts.append(num)
            found = False
            while not found:
                num += 1
                if "Calculation will run on" in lines[num]:
                    found = True
                    ends.append(num+1)
                    line = lines[num]

        # Special Matrices
        if "MO Eigenvalues" in line:
            starts.append(num+1)
            found = False
            while not found:
                num += 1
                if "MO Coefficients" in lines[num]:
                    found = True
                    ends.append(num)
                    line = lines[num]
            
        if "MO Coefficients" in line:
            starts.append(num+1)
            found = False
            while not found:
                num += 1
                if "Density Matrix" in lines[num]:
                    found = True
                    ends.append(num)
                    line = lines[num]
        # Matrices
        if regex_pattern6.match(line):
            #eigcheck = lines[num+NBasis+1]
            #if regex_pattern6.match(eigcheck):
            coefcheck = lines[num-1]
            if not "Coefficients" in coefcheck:
                starts.append(num)
                ends.append(num + matsize6)
                num += matsize6 - 1
            else:
                # We do Coefficients Matrices
                starts.append(num)
                marker = num
                found = False
                while not found:
                    num += 1
                    if "Density Matrix" in lines[num]:
                        found = True
                        ends.append(num)
                        num = marker+1
        elif regex_pattern4.match(line):
            # We do Alpha Fock Matrices
            starts.append(num)
            ends.append(num + matsize4)
            num += matsize4 - 1
        num += 1

    #print '\n'.join(["%d %d" % (s,e) for s,e in zip(starts, ends)])

    command = ['%d,%dfold' % (s, e) for s, e in zip(starts, ends)]
    command = '|'.join(command)
    command = 'vim +"%s|mkview" %s' % (command, fname)
    print command
    os.system(command)
    #command = command.split()


