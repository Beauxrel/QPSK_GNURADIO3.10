# this module will be imported in the into your flowgraph
# Returns a vector with the M-PSK complex symbols
# M: Modulation index (M=2: BPSK, M=4: QPSK, etc)

import numpy
import cmath

def PSKsymbols(M):
    if M==2:
       return [1, -1]
    else:
       lst = numpy.arange(M)
       return numpy.exp( (lst * 2j +1j) * cmath.pi/M )
