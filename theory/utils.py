from __future__ import division
import math

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def db_to_ebno(ebno_db):
    return 10.0**(ebno_db/10.0)

def find_ebno(ber,theory,speed=0.1):
    """
    Attempts to find the ebno associated with the given
    ber for the theory lambda
     ber: Bit Error Rate to find Eb/N0
     theory: lambda: (ebno)=>ber
    """
    ebno = 0
    while True:
        calc_ber = theory(ebno)
        if(isclose(calc_ber,ber)):
            break
        else:
            ebno = ebno + (calc_ber - ber)*0.1
    return ebno