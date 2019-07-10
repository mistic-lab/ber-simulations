from __future__ import division
import math
from .utils import db_to_ebno

def ber(M,ebno_db):
    ebno = db_to_ebno(ebno_db)

    # This function is here to match the definition mathworks used
    def Q(x):
        return math.erfc(x/math.sqrt(2.0))/2.0

    # Function of k
    def pb_k(k):    
        # Function i
        def pb_i(i):
            return ((-1.0)**(math.floor(i*2.0**(k-1)/M)))*\
            (2.0**(k-1)-math.floor(i*(2.0**(k-1))/M+0.5))*\
            Q((2.0*i+1.0)*math.sqrt(6.0*math.log(M,2)/(M**2.0-1.0)*ebno))
    
        # Inner Sum of i 
        return sum([pb_i(i) for i in range(0,int((1-2**-k)*M-1)+1)])
    
    # Outer sum of k and scaling factor
    pb_ksum = sum([pb_k(k) for k in range(1,int(math.log(M,2)+1))])
    return (2.0/(math.log(M,2)*M))*pb_ksum