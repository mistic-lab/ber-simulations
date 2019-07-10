from gnuradio import gr
from gnuradio import blocks

try:
    import tcola
except ImportError:
    print("Error: Program requires gr-tcola (https://github.com/mistic-lab/gr-tcola")
    sys.exit(1)


class TCOLAModWrapper(gr.hier_block2):
    """
    A modulation transceiver that wraps another modulation using TCOLA
    """
    def __init__(self,mod,m,r=1):
        gr.hier_block2.__init__(
            self, "TCOLA Mod Wrapper",
            gr.io_signaturev(2, 2, [gr.sizeof_char, gr.sizeof_gr_complex]),
            gr.io_signaturev(4, 4, [gr.sizeof_char,gr.sizeof_gr_complex, gr.sizeof_float, gr.sizeof_float]),
        )
        self.M=m
        self.R=r
        # Blocks
        self.mod = mod
        self.tc = tcola.time_compression_c(self.M,self.R,())
        self.ola = tcola.overlap_add_c(self.M,self.R,())
        self.tcola_delay = blocks.delay(gr.sizeof_gr_complex,1)

        # Connect the bit streams of tcola wrapper to mod block
        self.connect((self,0),(self.mod,0))
        self.connect((mod,0),(self,0))

        # Connect the TX & RX Symbol pads through to mod block
        self.connect((self.mod,2),(self,2))
        self.connect((self.mod,3),(self,3))

        # inject time compression after mod block tx signal
        self.connect((self.mod,1),self.tc)
        self.connect(self.tc,(self,1))

        # inject overlap and add before mod block rx signal
        self.connect((self,1),self.ola)
        self.connect(self.ola,self.tcola_delay)
        self.connect(self.tcola_delay,(self.mod,1))
    
    def get_bits_per_sym(self):
        return self.mod.get_bits_per_sym() if "get_bits_per_sym" in dir(self.mod) else 1
