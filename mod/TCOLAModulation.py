from .flowgraphs import TCOLAModWrapper
from .Modulation import Modulation

class TCOLAModulation(Modulation):
    def __init__(self,mod_block,m,r=1,options={},title="Untitled",n0_scale=1.0):
        Modulation.__init__(self,mod_block,options=options,title="%s TCOLA (M=%d,R=%d)"%(title,m,r),n0_scale=n0_scale)
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
