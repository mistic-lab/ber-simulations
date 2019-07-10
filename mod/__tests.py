from gnuradio import gr
from gnuradio import blocks
from gnuradio import filter
import numpy as np
from . import Modulation
import unittest

class invalid_mod_block(gr.hier_block2):
    """Invalid Mod Block Test Fixture
    """
    def __init__(self):
        gr.hier_block2.__init__(
            self, "Invalid BER Mod",
            gr.io_signaturev(2, 2, [gr.sizeof_gr_complex*1, gr.sizeof_char*1]),
            gr.io_signaturev(2, 2, [gr.sizeof_gr_complex*1, gr.sizeof_char*1]),
        )

class valid_mod_block(gr.hier_block2):
    """Valid Mod Block Test Fixture
    """
    def __init__(self):
        gr.hier_block2.__init__(
            self, "Valid BER Mod",
            gr.io_signaturev(2, 2, [gr.sizeof_char, gr.sizeof_gr_complex]),
            gr.io_signaturev(4, 4, [gr.sizeof_char,gr.sizeof_gr_complex,gr.sizeof_float,gr.sizeof_float]),
        )


class simple_mod(valid_mod_block):
    """Simple Modulation Block
    """
    def __init__(self,delay=0,amplitude=1):
        """Simple Modulation Block Fixture
        
        Keyword Arguments:
            delay {int} -- Delay to introduce (default: {0})
            amplitude {int} -- Amplitude Change (default: {1})
        """ 
        valid_mod_block.__init__(self)

        # Blocks
        self.b_to_f = blocks.char_to_float(1, 1)
        self.symbol_map_mult = blocks.multiply_const_vff((2.0, ))
        self.symbol_map_subtract = blocks.add_const_vff((-1.0,))
        self.delay_f = blocks.delay(gr.sizeof_float,delay=delay)
        self.f_to_c = blocks.float_to_complex(1)
        self.mult_f = blocks.multiply_const_vff((amplitude, ))
        
        self.c_to_r = blocks.complex_to_real(1)
        self.divide_f = blocks.multiply_const_vff((1.0/amplitude, ))
        self.symbol_map_add = blocks.add_const_vff((1.0,))
        self.symbol_map_divide = blocks.multiply_const_vff((1/2.0,))
        self.f_to_b = blocks.float_to_char(1,1)
        
        # Connections
        self.connect((self,0),self.b_to_f)
        self.connect(self.b_to_f,self.symbol_map_mult)
        self.connect(self.symbol_map_mult,self.symbol_map_subtract)
        self.connect(self.symbol_map_subtract,self.mult_f)
        self.connect(self.mult_f,(self,2))
        self.connect(self.mult_f,self.delay_f)
        self.connect(self.delay_f,self.f_to_c)
        self.connect(self.f_to_c,(self,1))

        self.connect((self,1),self.c_to_r)
        self.connect(self.c_to_r,self.divide_f)
        self.connect(self.divide_f,self.symbol_map_add)
        self.connect(self.symbol_map_add,self.symbol_map_divide)
        self.connect(self.symbol_map_divide,(self,3))
        self.connect(self.symbol_map_divide,self.f_to_b)        
        self.connect(self.f_to_b,(self,0))


class mod_block_with_fir(valid_mod_block):
    """Mod Block Fixture with an FIR Filter    
    """
    def __init__(self,samp_per_sym=1):
        valid_mod_block.__init__(self)

        # Blocks
        self.b_to_f = blocks.char_to_float(1, 1)
        self.interp_filter = filter.interp_fir_filter_fff(samp_per_sym, (np.ones(samp_per_sym)))
        self.f_to_c = blocks.float_to_complex(1)
        
        self.c_to_r = blocks.complex_to_real(1)
        self.decim_filter = filter.fir_filter_fff(samp_per_sym, (np.ones(samp_per_sym)))
        self.divide_f = blocks.multiply_const_vff((1.0/samp_per_sym, ))
        self.f_to_b = blocks.float_to_char(1,1)
        
        # Connections
        self.connect((self,0),self.b_to_f)
        self.connect(self.b_to_f,(self,2))
        self.connect(self.b_to_f,self.interp_filter)
        self.connect(self.interp_filter,self.f_to_c)
        self.connect(self.f_to_c,(self,1))

        self.connect((self,1),self.c_to_r)
        self.connect(self.c_to_r,self.decim_filter)
        self.connect(self.decim_filter,self.divide_f)
        self.connect(self.divide_f,(self,3))
        self.connect(self.divide_f,self.f_to_b)        
        self.connect(self.f_to_b,(self,0))


class TestValidateMod(unittest.TestCase):
    def test_valid_modulation(self):
        try:
            sim = Modulation(valid_mod_block)
            sim.validate_mod_block()
        except TypeError as ex:
            self.fail("Exception not expected: %s"%ex)
        

    def test_invalid_modulation(self):
        with self.assertRaises(TypeError) as ex:
            sim = Modulation(invalid_mod_block)
            sim.validate_mod_block()


# @unittest.skip("Skipping")
class TestModDelay(unittest.TestCase):
    
    def test_delay_is_correct(self):
        for delayVal in [2,6,11]:
            sim = Modulation(simple_mod,{"delay":delayVal})
            delay = sim.measure_delay()
            self.assertEqual(delay,delayVal)
    
    def test_block_with_fir(self):
        # val in (samples per symbol,expected_delay)
        for val in [(1,0),(2,1),(10,1)]:
            samp_per_sym,expected_delay = val
            sim = Modulation(mod_block_with_fir,{'samp_per_sym':samp_per_sym})
            delay = sim.measure_delay()
            self.assertEqual(delay,expected_delay)

# @unittest.skip("Skipping")
class TestEnergyPerBit(unittest.TestCase):
    def test_power_per_bit_is_correct(self):        
        for num_bits in [10,20,30]:
            for amp in [2,6,11]:
                sim = Modulation(simple_mod,{"amplitude":amp})
                eb = sim.measure_eb(num_bits=num_bits)
                expected_eb = (amp**2)*num_bits/float(num_bits)
                self.assertEqual(eb,expected_eb)