from __future__ import division
import math
from .utils import db_to_ebno


def ber(M,ebno_db):
    ebno = db_to_ebno(ebno_db)

    def binomial_coef(top,bot):
        return math.factorial(top)/(math.factorial(top-bot)*math.factorial(bot))

    def ps_m(m):
        return ((-1)**(m+1))*binomial_coef(M-1,m)*(1.0/(m+1))*math.exp(-1*(m*math.log(M,2)/(m+1)*ebno))
    
    # scaling factor * Sum
    return ((M/2)/(M-1))*sum([ps_m(m) for m in range(1,M)])