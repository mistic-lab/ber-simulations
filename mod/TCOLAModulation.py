from .flowgraphs import TCOLAModWrapper
from .Modulation import Modulation

class TCOLAModulation(Modulation):
    """TCOLA Modulation extends the original Modulation to wrap
    the modulation transceiver block with TCOLA
    """
    def __init__(self,mod_block,m,r=1,options={},title="Untitled"):
        """Creates a TCOLA Modulation from a modulation transceiver block
        
        Arguments:
            Modulation {[type]} -- [description]
            mod_block {Modulation Transceiver} -- The Modulation Transceiver Block
            m {int} -- Window Size
        
        Keyword Arguments:
            r {int} -- Hop Size (default: {1})
            options {dict} -- Options to be passed to the Modulation Transceiver (default: {{}})
            title {str} -- Title of Modulation (default: {"Untitled"})
        """
        Modulation.__init__(self,mod_block,options=options,title="%s TCOLA (M=%d,R=%d)"%(title,m,r))
        self.M = m
        self.R = r
    
    def _create_mod_block(self):
        # Wrap the original modulation block in the TCOLA Mod Wrapper
        mod = Modulation._create_mod_block(self)
        return TCOLAModWrapper(mod,self.M,self.R)
    
    def get_tcola_num_samples(self,num_samples):
        return int(num_samples*float(self.M)/float(self.R))

    def measure_delay(self,num_bits=None):
        tcola_num_samples = num_bits if num_bits is not None else self.get_tcola_num_samples(self.M)
        return Modulation.measure_delay(self,num_samples=tcola_num_samples)
    
    def measure_eb(self,num_bits=None):
        tcola_num_bits = num_bits if num_bits is not None else self.get_tcola_num_samples(self.M)
        return Modulation.measure_eb(self,num_bits=tcola_num_bits)
