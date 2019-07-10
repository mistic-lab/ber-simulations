from gnuradio import gr
from gnuradio import blocks
from gnuradio import digital
import numpy as np
from .ModMeasurement import ModMeasurementGraph

class EbMeasurementGraph(ModMeasurementGraph):
    def __init__(self,mod,num_bits=1000):
        ModMeasurementGraph.__init__(self,mod, "Eb Measurement")
        self.num_bits=num_bits
        # self.bitSrc = blocks.vector_source_b(get_random_bits(num_bits).tolist(), True)
        self.bitSrc = digital.glfsr_source_b(8, True, 0, 1)
        self.src = blocks.head(gr.sizeof_char,num_bits)
        self.nop_c = blocks.delay(gr.sizeof_gr_complex,0)        
        self.null_sink_b = blocks.null_sink(gr.sizeof_char)
        self.power = blocks.complex_to_mag_squared(1)
        self.dest = blocks.vector_sink_f()                
        
        # Connections
        self.connect(self.bitSrc,self.src)
        self.connect(self.src,self.mod_in_bits)
        self.connect(self.mod_out_signal,self.power)
        self.connect(self.power,self.dest)

        # Only care about the power output of the transmission pad
        # null sink / source the other inputs/outputs
        self.connect(self.mod_out_signal,self.nop_c)
        self.connect(self.nop_c,self.mod_in_signal)
        self.connect(self.mod_out_bits,self.null_sink_b)     
    
    def measure(self):
        self.run()
        result_data = self.dest.data()[:]
        return sum(result_data)/float(self.num_bits)