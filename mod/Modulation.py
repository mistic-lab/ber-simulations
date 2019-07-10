from threading import Thread,Event,Lock
from gnuradio import gr
from .flowgraphs import EbMeasurementGraph, DelayMeasurementGraph, BERMeasurementGraph

class Modulation(object):
    """Modulation Transceiver BER Simulation 

    Responsible for simulating and measuring bit error rates for a given 
    modulation transceiver block.
    """
    def __init__(self,mod_block,options={},title="Untitled",n0_scale= 1.0):
        """Constructor for a Modulation object
        
        Arguments:
            mod_block {Modulation} -- Modulation Transceiver block class
        
        Keyword Arguments:
            options {dict} -- Options passed into instances of the Modulation Transceiver Block (default: {{}})
            title {str} -- Title of the simulation (default: {"Untitled"})
        """
        object.__init__(self)
        self.__thread_lock = Lock()
        self.n0_scale = n0_scale
        self.title = title
        self.mod_block = mod_block
        self.mod_options = options
        self.mod_delay = None
        self.mod_eb = None
        self.is_mod_valid = None

    def initialize(self):
        with self.__thread_lock:
            if self.is_mod_valid is None:
                self.validate_mod_block()
                self.is_mod_valid = True
            if self.mod_delay is None:
                self.mod_delay = self.measure_delay()
            if self.mod_eb is None:
                self.mod_eb = self.measure_eb()

    def _create_mod_block(self):
        return self.mod_block(**self.mod_options)

    def validate_mod_block(self):
        """Validates the structure of the given Modulation Transceiver
        Raises:
            TypeError: Error describing the problem with the Modulation Transciever IO Signature
        """
        mod = self._create_mod_block()
        in_sig = mod.input_signature()
        if mod.input_signature().sizeof_stream_item(0) is not gr.sizeof_char:
            raise TypeError("Incorrect input signature: First input must accept byte stream")
        if mod.input_signature().sizeof_stream_item(1) is not gr.sizeof_gr_complex:
            raise TypeError("Incorrect input signature: Second input must accept complex stream")

        if mod.output_signature().sizeof_stream_item(0) is not gr.sizeof_char:
            raise TypeError("Incorrect output signature: First output must be byte stream")
        if mod.output_signature().sizeof_stream_item(1) is not gr.sizeof_gr_complex:
            raise TypeError("Incorrect output signature: Second output must be complex stream")
        if mod.output_signature().sizeof_stream_item(2) is not gr.sizeof_float:
            raise TypeError("Incorrect output signature: Third output must be a stream of floats representing TX Symbols")
        if mod.output_signature().sizeof_stream_item(3) is not gr.sizeof_float:
            raise TypeError("Incorrect output signature: Fourth output must be a stream of floats representing RX Symbols")

    def measure_delay(self,num_samples=100):
        """Measure inherent delay of Modulation Transceiver
        
        Keyword Arguments:
            num_samples {int} -- Number of samples to use when measuring delay (default: {100})
        
        Returns:
            {int} -- The number of samples of delay introduced by the Modulation Transceiver 
        """
        mod = self._create_mod_block()
        delay_graph = DelayMeasurementGraph(mod,num_samples=num_samples)
        symbol_delay = delay_graph.measure()
        bits_per_sym = mod.get_bits_per_sym() if 'get_bits_per_sym' in dir(mod) else 1
        return int(symbol_delay*bits_per_sym)

    def measure_eb(self, num_bits=1000):
        """Measure the Energy per Bit of the Modulation Transceiver
        
        Keyword Arguments:
            num_bits {int} -- Number of samples to use when measuring the Energy per Bit (default: {1000})
        
        Returns:
            float -- Energy contained within 1 bit
        """
        mod = self._create_mod_block()
        eb_graph = EbMeasurementGraph(mod,num_bits)
        eb =  eb_graph.measure()
        return eb

    def measure_ber(self,ebno_db,on_progress=None):
        """Calculate the Bit Error Rate for the Modulation Transciever
        
        Arguments:
            ebno_db {float} -- Eb/N0 (dB) to calculate the BER for
        
        Keyword Arguments:
            on_progress {lambda:(num_errors)} -- Progress call back for updates with the current number of bit errors (default: {None})
        
        Returns:
            float -- The Bit Error Rate
        """
        self.initialize()       
        ebno = 10.0**(ebno_db/10.0)
        n_0 = self.mod_eb/ebno
        mod = self._create_mod_block()     
        ber_graph = BERMeasurementGraph(mod,self.mod_delay,n_0*self.n0_scale)
        ber = ber_graph.measure(on_progress=on_progress) 
        return ber

