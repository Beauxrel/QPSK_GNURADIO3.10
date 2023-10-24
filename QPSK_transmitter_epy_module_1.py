# this module will be imported in the into your flowgraph

# Returns a vector of a decimal set of Gray codes of n binary digits
# n: The binary digits length of the Gray code

def gray_code(n):
    if n <= 0:
        return []
    if n == 1:
        return ['0', '1']
    res = gray_code(n-1)
    return ['0'+s for s in res] + ['1'+s for s in res[::-1]]

def bin_to_gray(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    a = MSB(n) # Assume MSB function exists. It find MSB of n
    b = n - 2**a
    return 2**a + bin_to_gray(2**a-1-b)

import math
# A simple way to find MSB
def MSB(n):
    return int( math.log(n, 2.0) )

def gray2int(n):
    A = []
    for k in range(2**n):
        A.append(bin_to_gray(k))
    return A
