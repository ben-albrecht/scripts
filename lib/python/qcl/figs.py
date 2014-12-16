#!/usr/bin/env python
# encoding: utf-8

try:
    import sys
    import cclib, argparse
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.axes as ax
except ImportError:
    raise ImportError('Unable to import all libraries')

#
#class qcdata(ccdata):
#
#    """sub-class of ccdata with plot data"""
#
#    def __init__(self, *args, **kwargs):
#        """Initialize
#
#
#        """
#        ccdata.__init__(self, *args, **kwargs)


def opt(ccinput):
    """Generate plots of convergence criteria, and energy vs. optimization cycles

    :job: ccdata object, or file
    :returns: TODO

    """

    if type(ccinput) == str:
        # Assuming ccinput is a filename
        data = cclib.parser.ccopen(ccinput).parse()
    else:
        data = ccinput
        assert type(data) == cclib.parser.data.ccData_optdone_bool

    criteria = [0,0,0]
    criteria[0] = [x[0] for x in data.geovalues]
    criteria[1] = [x[1] for x in data.geovalues]
    criteria[2] = [x[2] for x in data.geovalues]
    idx = np.arange(len(criteria[0]))

    # Plot Geometry Optimization Criteria for Convergence over opt cycles
    plt.plot(idx, criteria[0], label='Gradient')
    plt.plot(idx, criteria[1], label='Displacement')
    plt.plot(idx, criteria[2], label='Energy Change')

    # Plot target criteria for convergence
    plt.axhline(y=data.geotargets[0])
    plt.yscale('log')


    plt.title("Optimization Convergence Analysis")
    plt.xlabel("Optimization Cycle")

    plt.legend()
    plt.show()

    idx = np.arange(len(data.scfenergies))
    plt.plot(idx, data.scfenergies, label='SCF Energy (eV)')
    plt.show







def main():
    """
    Main function
    TODO - Determine jobtype using cclib
    """

    opt("ts1.3.0.out")




if __name__ == '__main__':
    main()
