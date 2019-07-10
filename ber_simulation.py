#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Ber Test Block
# Generated: Tue Jun 11 15:07:29 2019
##################################################

import os
import sys
import re

try:
    from matplotlib import pyplot as plt
except ImportError:
    print("Error: Program requires Matplotlib (matplotlib.sourceforge.net).")
    sys.exit(1)

sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

# from threading import Thread,Event
from multiprocessing import cpu_count


from curve import BERSimulationManager
import theory
from mod import Modulation, TCOLAModulation
from grc import (
    ber_mod_bpsk_square,
    ber_mod_bpsk_rrc
)


# from ber_mod_bpsk_square import ber_mod_bpsk_square
# from ber_mod_bpsk_rrc import ber_mod_bpsk_rrc
from ber_mod_4pam_square import ber_mod_4pam_square
from ber_mod_4pam_rrc import ber_mod_4pam_rrc
from ber_mod_2fsk_square import ber_mod_2fsk_square
from ber_mod_2fsk_rrc import ber_mod_2fsk_rrc
from ber_mod_4fsk_square import ber_mod_4fsk_square
from ber_mod_4fsk_rrc import ber_mod_4fsk_rrc

import time
import math
import numpy as np

def main():    
    

    ebn0_dbs = np.arange(0.0,12.0)
    
    # ebn0_dbs = [12.0]

    tcola_ms = [16,32,64]

    print_status = False
    # print_status = True

    create_plots = True
    # create_plots = False

    create_data_file = True

    enable_square_pulse = False
    enable_rrc_pulse = False

    # enable_square_pulse = True
    enable_rrc_pulse = True

    enable_bpsk = False
    enable_4pam = False
    enable_2fsk = False
    enable_4fsk = False

    # enable_bpsk = True
    enable_4pam = True
    # enable_2fsk = True
    # enable_4fsk = True

    num_sims = cpu_count()
    num_sims = 4

    samps_per_sym = []

    simManager = BERSimulationManager(ebn0_dbs,num_sims,results_dir="./results/")

    data = {}
    data['ebno_db'] = ebn0_dbs

    def plot_theoretical(ebno_dbs=[], bpsk=False,four_pam=False,two_fsk=False,four_fsk=False,verbose=False):
        ebn0s = [10**(ebn0_db/10.0) for ebn0_db in ebn0_dbs]
        if verbose:
            print("EBNOS",ebn0s)
        if bpsk:
            # Theoretical BPSK Performance
            ber_bpsk_theor = [theory.ber_bpsk(ebno_db) for ebno_db in ebn0_dbs]
            plt.semilogy(ebn0_dbs,ber_bpsk_theor,label="Theoretical BPSK")
            if verbose:
                print("BPSK Theory",ber_bpsk_theor)

        if four_pam:
            # Theoretical 4PAM
            ber_4pam_theory = [theory.ber_mpam(4,ebno_db) for ebno_db in ebn0_dbs]
            plt.semilogy(ebn0_dbs,ber_4pam_theory,label="Theoretical 4PAM")
            if verbose:
                print("4PAM Theory",ber_4pam_theory)

        if two_fsk:
            # Theoretical 2FSK
            ber_2fsk_theory = [theory.ber_mfsk(2,ebno_db) for ebno_db in ebno_dbs]
            matlab_theory = [
                0.0493758144766571,
                0.0370483379796805,
                0.0261808188053516,
                0.0171770521157097,
                0.0102767791530923,
                0.00548125546503938,
                0.00253301373230551,
                0.000978427158791110,
                0.000301918068199750,
                7.02965217251387e-05
            ]
            plt.semilogy(ebn0_dbs,ber_2fsk_theory,label="Theoretical NC 2FSK")
            plt.semilogy(ebn0_dbs,matlab_theory,label="Matlab NC 2FSK")
            if verbose:
                print("2FSK Theory",ber_2fsk_theory)

        if four_fsk:
            # Theoretical 4FSK
            ber_4fsk_theory = [theory.ber_mfsk(4,ebno_db) for ebno_db in ebno_dbs]
            plt.semilogy(ebn0_dbs,ber_4fsk_theory,label="Theoretical NC 4FSK")
            if verbose:
                print("4FSK Theory",ber_4fsk_theory)

    def create_standard_simulations(mod,title,in_memory=True,samps_per_sym=[],tcola_ms=tcola_ms):
        for sps in samps_per_sym:
            options={'samp_per_sym':sps}
            sim_title="%s (SPS=%d)"%(title,sps)
            simManager.add_simulation(
                Modulation(mod,options,title=sim_title),
                in_memory=in_memory
            )
            for m in tcola_ms:
                simManager.add_simulation(
                    TCOLAModulation(mod,m=m,options=options,title=sim_title),
                    in_memory=in_memory
                )

    if enable_bpsk:
        if enable_square_pulse:
            # BPSK with Square Pulses
            create_standard_simulations(ber_mod_bpsk_square,"BPSK Square",samps_per_sym=[1,4,8],in_memory=False)

        if enable_rrc_pulse:
            # BPSK with RRC Pulses
            create_standard_simulations(ber_mod_bpsk_rrc,"BPSK RRC",samps_per_sym=[8,16],in_memory=False)

    if enable_4pam:
        if enable_square_pulse:
            # 4PAM with Square Pulses
            create_standard_simulations(ber_mod_4pam_square,"4PAM Square",samps_per_sym=[1,4,8],in_memory=False)

        if enable_rrc_pulse:
            # 4PAM with RRC Pulses
            create_standard_simulations(ber_mod_4pam_rrc,"4PAM RRC",samps_per_sym=[8,16],in_memory=False)

    if enable_2fsk:
        # 2FSK with Square Pulses
        # create_standard_simulations(ber_mod_bpsk_square,"BPSK Square",samps_per_sym=[1,4,8],in_memory=False)

        # BPSK with RRC Pulses
        # create_standard_simulations(ber_mod_bpsk_rrc,"BPSK RRC",samps_per_sym=[8,16],in_memory=False)

        simManager.add_simulation(Simulation(ber_mod_2fsk_square,{"samp_per_sym":8},title="2FSK Square"))

        simManager.add_simulation(Simulation(ber_mod_2fsk_rrc,{"samp_per_sym":8},title="2FSK RRC"))

    simManager.generate_curves(print_status=True)

    for curve in simManager.curveSimulations:
        print(curve.title) 
        print("DELAY",curve.simulation.mod_delay,"Eb",curve.simulation.mod_eb)
       
        bers = curve.get_bers(ebn0_dbs) 
        plt.semilogy(ebn0_dbs,bers,label=curve.title,marker='o')


    plot_theoretical(
        ebn0_dbs,
        bpsk=enable_bpsk,
        two_fsk=enable_2fsk,
        four_fsk=enable_4fsk,
        four_pam=enable_4pam,
        verbose=False
    )

    plt.legend(loc='lower left')
    plt.show()

    return

if __name__ == '__main__':
    main()