from gnuradio import gr

class ModMeasurementGraph(gr.top_block):
    def __init__(self,mod,name="Mod Measurement Graph"):
        gr.top_block.__init__(self,name)
        self.mod = mod

    @property
    def mod_bits_per_sym(self):
        if("get_bits_per_sym" in self.mod):
            return self.mod.get_bits_per_sym()
        else:
            return 1

    @property
    def mod_in_bits(self):
        return (self.mod,0)
    
    @property
    def mod_in_signal(self):
        return (self.mod,1)

    @property
    def mod_out_bits(self):
        return (self.mod,0)

    @property
    def mod_out_signal(self):
        return (self.mod,1)

    @property
    def mod_out_symbols_tx(self):
        return (self.mod,2)

    @property
    def mod_out_symbols_rx(self):
        return (self.mod,3)