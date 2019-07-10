import unittest
import numpy as np
from mod import Modulation, TCOLAModulation
from mod.flowgraphs.utils import isclose
import theory

from . import ber_mod_bpsk_square


class TestBPSK(unittest.TestCase):
    def get_simulation(self,options={}):
        return Modulation(ber_mod_bpsk_square,options)

    def test_valid(self):
        sim = self.get_simulation()
        try:
            sim.validate_mod_block()
        except Exception as e:
            self.fail("Invalid Block",e)

    def test_samp_per_sym(self):
        for sps in [1,3,4,5,6,7]:
            sim = self.get_simulation({"samp_per_sym":sps})
            eb = sim.measure_eb()
            self.assertEqual(eb,sps)
            delay = sim.measure_delay()
            self.assertEqual(delay,1 if sps != 1 else 0)

    @unittest.skip("These Don't work but we should compare to theory here")
    def test_ber_measure(self):
        for sps in [1,5,8,16]:
            sim = self.get_simulation({"samp_per_sym":sps})
            eb = sim.measure_eb()
            delay = sim.measure_delay()
            print("EB",eb,"DELAY",delay)
            for ebnodb in [0,2,4,8]:
                ebno = 10**(ebnodb/10.0)
                n_0 = eb/ebno
                ber,errors = sim.measure_ber(ebnodb)
                ber_theory = theory.ber_bpsk(ebno)
                err = abs(ber-ber_theory)/ber_theory
                self.assertTrue(isclose(ber,ber_theory,rel_tol=0.7),msg="BER didn't match theory for sps=%d ebnodb=%d\r\n %f != %f (theory) " %(sps,ebnodb,ber,ber_theory))

@unittest.skip("Skipping")
class TestTcolaBPSK(unittest.TestCase):
    def get_simulation(self,m=1,r=1,options={}):
        return TCOLAModulation(ber_mod_bpsk_square,m,r,options)

    def test_valid(self):
        sim = self.get_simulation()
        try:
            sim.validate_mod_block()
        except Exception as e:
            self.fail("Invalid Block",e)

    @unittest.skip("For Debugging")
    def test_samp_per_sym(self):
        for sps in [1,8]:
            for m in [16,30]:
                sim = self.get_simulation(m=m,options={"samp_per_sym":sps})
                eb = sim.measure_eb()
                delay = sim.measure_delay(40)
                print("EB",eb,"DELAY",delay)
                # self.assertEqual(delay, 1 if m <= sps else int(m/sps)+1,"Delay assertion failed for m=%d sps=%d"%(m,sps))
    
    def test_ber_measure(self):
        for m in [8,16]:
            for sps in [1,5,8,16]:
                sim = self.get_simulation(m,options={"samp_per_sym":sps})
                eb = sim.measure_eb()
                delay = sim.measure_delay()
                print("EB",eb,"DELAY",delay)
                for ebnodb in [0,2,4,8]:
                    ebno = 10**(ebnodb/10.0)
                    n_0 = eb/ebno
                    ber,errors = sim.measure_ber(ebnodb)
                    ber_theory = theory.ber_bpsk(ebno)
                    print("N_0",n_0,"BER",ber,ber_theory)
                    err = abs(ber-ber_theory)/ber_theory
                    
                    self.assertLessEqual(err,0.25,msg="BER didn't match theory for sps=%d ebnodb=%d\r\n %f != %f " %(sps,ebnodb,ber,ber_theory))

@unittest.skip("Skipping")
class Test2FSK(unittest.TestCase):
    def get_simulation(self,options={}):
        return Modulation(ber_modulation_2fsk,options)

    def test_valid(self):
        sim = self.get_simulation()
        try:
            sim.validate_mod_block()
        except Exception as e:
            self.fail("Invalid Block",e)

    def test_samp_per_sym(self):
        for sps in [1,4,20]:
            sim = self.get_simulation({"samp_per_sym":sps})
            eb = sim.measure_eb()
            self.assertAlmostEqual(eb,sps,4)
            delay = sim.measure_delay(30)
            self.assertEqual(delay,1) 

@unittest.skip("Skipping")
class TestTcol2FSK(unittest.TestCase):
    def get_simulation(self,m=1,r=1,options={}):
        return TCOLAModulation(ber_modulation_2fsk,m,r,options)

    def test_valid(self):
        sim = self.get_simulation()
        try:
            sim.validate_mod_block()
        except Exception as e:
            self.fail("Invalid Block",e)

    # @unittest.skip("Debugging")
    def test_samp_per_sym(self):
        for sps in [1,4,8]:
            for m in [8,16,30]:
                print("SPS",sps,"M",m)
                sim = self.get_simulation(m=m,options={"samp_per_sym":sps})
                eb = sim.measure_eb()
                delay = sim.measure_delay(40)
                print("EB",eb,"DELAY",delay)
                # self.assertEqual(delay, 1 if m <= sps else int(m/sps)+1,"Delay assertion failed for m=%d sps=%d"%(m,sps))
