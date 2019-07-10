from __future__ import division
import math
from .utils import db_to_ebno

def ber(ebno_db):
    ebno = db_to_ebno(ebno_db)
    return 0.5*math.erfc(math.sqrt(ebno))