import unittest
import numpy as np
from . import find_ebno, ber_bpsk, ber_mfsk, ber_mpam

class TestTheory(unittest.TestCase):
    def test_find_ebno(self):
        ebno = 1.0
        ber = ber_bpsk(ebno)
        calc_ebno = find_ebno(ber,ber_bpsk)
        self.assertAlmostEqual(ebno,calc_ebno)
    
    def test_4pam(self):
        ebnos = np.arange(0.0,10.0)
        matlab_results = [
                0.140981635066842,	
                0.118997407465924,	
                0.0977418537374870,	
                0.0774530602925490,	
                0.0586237372834044,	
                0.0418927600464623,	
                0.0278713278451503,	
                0.0169667343687604,	
                0.00924721374147442,
                0.00439033608735211
        ]
        for i,ebno in enumerate(ebnos):
            self.assertAlmostEqual(matlab_results[i],ber_mpam(4,ebno))

    def test_4fsk(self):
        ebnos = np.arange(0.0,10.0)
        matlab_results = [
            0.229336375785696,	
            0.184750786709468,	
            0.139868054517323,	
            0.0977191631133165,	
            0.0615567228721839,	
            0.0339459636328800,	
            0.0157897496300472,	
            0.00591388054418751,
            0.00168372668630849, 
            0.000339394050689889
        ]
        for i,ebno in enumerate(ebnos):
            self.assertAlmostEqual(matlab_results[i],ber_mfsk(4,ebno))


if __name__ == '__main__':
    unittest.main()
