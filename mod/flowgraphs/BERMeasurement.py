from threading import Thread
from gnuradio import gr
from gnuradio import blocks
from gnuradio import digital
from gnuradio import analog
from gnuradio import fec
import time
import math
import numpy as np
from .ModMeasurement import ModMeasurementGraph

class BERMeasurementGraph(ModMeasurementGraph):
    def __init__(self,mod,delay=0,n_0=0,min_errors=100):
        ModMeasurementGraph.__init__(self, mod, "BER Measurement")
        self.__probe_thread = None
        self._did_timeout = False  
                
        # Blocks
        self.src = digital.glfsr_source_b(8, True, 0, 1)
        # self.src = blocks.vector_source_b(np.concatenate((np.ones(5,dtype='B'),np.zeros(10,dtype='B'))).tolist(),True)
        # self.src = blocks.vector_source_b(np.zeros(10,dtype='B').tolist(),True)
        self.noise = analog.noise_source_c(analog.GR_GAUSSIAN, math.sqrt(float(n_0)), 0)
        self.delay = blocks.delay(gr.sizeof_char,delay)
        self.add = blocks.add_vcc(1)
        self.skiphead_orig = blocks.skiphead(gr.sizeof_char,500)
        self.skiphead_rx = blocks.skiphead(gr.sizeof_char,500)

        self.pack_rx_bits = blocks.pack_k_bits_bb(8)
        self.pack_msg_bits = blocks.pack_k_bits_bb(8)
        self.ber_measure = fec.ber_bf(True, min_errors, -7.0)
        self.ber_sink = blocks.vector_sink_f(1)
                
        # Connections
        self.connect(self.src,self.mod_in_bits)

        # Adding noise to tx output of mod
        self.connect(self.mod_out_signal,(self.add,0))
        self.connect(self.noise,(self.add,1))
        self.connect(self.add,self.mod_in_signal)

        # Rx bits from mod to ber measure
        self.connect(self.mod_out_bits,self.skiphead_rx)
        self.connect(self.skiphead_rx,self.pack_rx_bits)
        self.connect(self.pack_rx_bits,(self.ber_measure,1))

        # delayed bits to ber measure
        self.connect(self.src,self.delay)
        self.connect(self.delay,self.skiphead_orig)
        self.connect(self.skiphead_orig,self.pack_msg_bits)
        self.connect(self.pack_msg_bits,(self.ber_measure,0))  
        self.connect(self.ber_measure,self.ber_sink)

    def probe_progress(self,on_progress,on_timeout):
        elapsed = 0
        while True:
            total_errors = self.ber_measure.total_errors()
            bers = self.ber_sink.data()
            if(total_errors == 0):
                elapsed = elapsed + 1
            if elapsed > 250:
                on_timeout()
                break
            
            if on_progress is not None:
                on_progress(total_errors)
            
            # If the BER Module produces a value, stop probing
            if(len(bers)>0):
                self.stop()
                break
             
            time.sleep(1.0 / (10))
    
    def on_timeout(self):
        print("Timeout!")
        self._did_timeout = True
        self.stop()
       
    def measure(self,on_progress=None):
        # Setup Probe thread
        self.__probe_thread = Thread(target=self.probe_progress,args=(on_progress,self.on_timeout))
        self.__probe_thread.setDaemon(True)
        self.__probe_thread.start()
        
        # Run Flowgraph
        self.run()        
        self.__probe_thread.join()
        if(self._did_timeout):
            raise Exception("Timeout")

        ber_result = self.ber_sink.data()[0]
        return 10.0**ber_result, self.ber_measure.total_errors()