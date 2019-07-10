class ErrorRateMeasurementGraph(ModMeasurementGraph):
    def __init__(self,mod,delay=0,skip=1000,num_samples=10000):
        ModMeasurementGraph.__init__(self, mod, "BER Measurement")

        # Blocks
        self.src = blocks.vector_source_b(np.random.randint(0,2,num_samples+skip,dtype='B').tolist())
        # self.src = digital.glfsr_source_b(8, True, 0, 1)
        self.nop_c = blocks.delay(gr.sizeof_gr_complex,0)
        self.delay = blocks.delay(gr.sizeof_char,delay)

        self.skiphead_orig = blocks.skiphead(gr.sizeof_char, skip)
        self.skiphead_rx = blocks.skiphead(gr.sizeof_char, skip)

        self.pack_rx_bits = blocks.pack_k_bits_bb(8)
        self.pack_msg_bits = blocks.pack_k_bits_bb(8)
        self.ber_measure = fec.ber_bf(False, 100, -7.0)
        self.ber_sink = blocks.vector_sink_f(1)

        # Connections
        # self.connect(self.src,self.head)
        self.connect(self.src,self.mod_in_bits)
        self.connect(self.mod_out_signal,self.nop_c)
        self.connect(self.nop_c,self.mod_in_signal)
        
        # delayed bits to ber measure
        self.connect(self.src,self.delay)
        self.connect(self.delay,self.skiphead_orig)
        self.connect(self.skiphead_orig,self.pack_msg_bits)
        self.connect(self.pack_msg_bits,(self.ber_measure,0))  

        # Rx bits from mod to ber measure
        self.connect(self.mod_out_bits,self.skiphead_rx)
        self.connect(self.skiphead_rx,self.pack_rx_bits)
        self.connect(self.pack_rx_bits,(self.ber_measure,1))
        self.connect(self.ber_measure,self.ber_sink)
        # self.connect(self.head,self.ber_sink)

    def measure(self):
        self.run()
        bers = self.ber_sink.data()
        return np.average([10**ber for ber in bers]) 