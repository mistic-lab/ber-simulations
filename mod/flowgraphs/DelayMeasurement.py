from gnuradio import gr
from gnuradio import blocks
from .ModMeasurement import ModMeasurementGraph
import numpy as np
from .utils import isclose

class DelayMeasurementGraph(ModMeasurementGraph):
    def __init__(self,mod,num_samples=100):
        ModMeasurementGraph.__init__(self, mod, "Mod Delay Measurment Graph")       
        # self.src = digital.glfsr_source_b(8, True, 0, 1)
        self.head = blocks.head(gr.sizeof_char, num_samples)
        self.nop_c = blocks.delay(gr.sizeof_gr_complex,0)
        self.null_sink = blocks.null_sink(gr.sizeof_char)
        self.src = blocks.vector_source_b(np.ones(num_samples,dtype='B').tolist())

        self.tx_symbols = blocks.vector_sink_f(1)
        self.rx_symbols = blocks.vector_sink_f(1)

        # Connections
        self.connect(self.src,self.head)
        self.connect(self.head,self.mod_in_bits)
        self.connect(self.mod_out_symbols_tx,self.tx_symbols)
        self.connect(self.mod_out_symbols_rx,self.rx_symbols)
        self.connect(self.mod_out_signal,self.nop_c)
        self.connect(self.nop_c,self.mod_in_signal)
        self.connect(self.mod_out_bits,self.null_sink)
    
    def measure(self):
        self.run()
        # orig,processed = self.bit_sink.data  
        orig = self.tx_symbols.data()
        processed = self.rx_symbols.data()          

        # print(orig)
        # print(processed)
        # isClose = [isclose(orig[0],val,rel_tol=0.5)for val in processed] 
        # print(isClose)

        # Find the first instance of the first symbol
        # in the received symbols.  Check for equality based on the value being within 1% of original value
        delay = 0
        try:
            delay = next((index for index,val in enumerate(processed) if isclose(orig[0],val,rel_tol=0.35)))
        except StopIteration:
            pass

        return delay    