from __future__ import division
import math

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def get_random_bits(length):
    return np.random.randint(0,2,length,dtype='B')