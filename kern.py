#!/usr/bin/env python
# encoding: utf-8

"""
Utility script for presenting my local benchmarks data
"""


from os import listdir, path


def average(numbers):
    """Compute average (didn't want to dep on numpy)"""
    return sum(numbers) / len(numbers)


def parseoutput(output, r=5):
    """Parse rates and average timings output from kernel"""
    timingsoutput = [x for x in output.split('\n') if 'Rate' in x]
    # Parse rates and timings
    rates = []
    avgtimes = []
    for line in timingsoutput:
        rates.append(float(line.split()[2]))
        avgtimes.append(float(line.split()[6]))

    # Pop first r data points to account for 'warm-up' iterations
    rates = rates[r:]
    avgtimes = avgtimes[r:]

    return(rates,avgtimes)


def processlogfile(logfile):
    """Process output and compute averages of rates/timings"""
    with open(logfile, 'r') as log:
        output = log.read()
        rates, avgtimes = parseoutput(output)
        avgrate = average(rates)
        avgtime = average(avgtimes)

    return avgrate


def process(kernel):
    """Construct nested dicts for kernel->machine->version->data"""
    kernelpath = path.abspath(kernel)
    kerneldata = {}
    for machinepath in [path.join(kernelpath, x) for x in listdir(kernel)]:
        machine = path.split(machinepath)[1]
        machinedata = {}
        for logfile in [path.join(machinepath, x) for x in listdir(machinepath)]:
            logname = path.split(logfile)[1].split('.')[0]
            machinedata[logname] = processlogfile(logfile)

        kerneldata[machine] = machinedata
    return kerneldata


def prettyprint(kerneldata):
    """Print kernel data nicely"""
    for machine, data in kerneldata.items():
        print(machine, '\n')
        try:
            print('  Serial:')
            chpldata, Cdata = (data['chpl-serial'], data['C-serial'])
            print('      chpl:', chpldata)
            print('      C   :', Cdata)
            print('    chpl/C:', chpldata / Cdata, '\n')
        except:
            print('    [No data]')

        try:
            print('  Shared:')
            chpldata, Cdata = (data['chpl-shared'], data['C-shared'])
            print('      chpl:', chpldata)
            print('      C   :', Cdata)
            print('    chpl/C:', chpldata / Cdata, '\n')
        except:
            print('    [No data]')

        try:
            print('  Multilocale:')
            blockdist, stencildist, Cdata = (data['chpl-blockdist'],data['chpl-stencildist'], data['C-shared'])
            print('     block:', blockdist)
            print('   stencil:', stencildist)
            print('      C   :', Cdata)
            print('   block/C:', blockdist / Cdata)
            print(' stencil/C:', stencildist / Cdata, '\n')
        except:
            print('    [No data]')

