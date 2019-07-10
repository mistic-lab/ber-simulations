# PyBerGr

> Pronounced *Pie Burger*

A python based framework for running GNU Radio based ber simulations on general modulations developed in Gnu Radio Companion.

Requirements:

- Should have GNU Radio Installed
- Should Also have [gr-tcola](https://github.com/mistic-lab/gr-tcola) Installed
- There are probably a few other GNU Radio blocks that might need to be installed
- Build all of the *heir* blocks so that the appropriate code ends up in the `.grc_gnuradio` path

# Scripts

Can run the build and test scripts using `./scripts.sh`

- **build** - Build all of the `grc` hierarchical and modulation transceiver blocks needed for the simulations
- **Test**  - Test the framework parts

# Demo

- Run `./scripts.sh build`
- Run `python ber_simulation.py` to generate some BER Curves

Future Work:

- Test this library with Python 3
- Test using this library as a package
- Would be great to write tests for the modulation GRC's that compare BER results against theory, some of these have been written but are being skipped as they always fail for some reason
- Finish the Transceivers for `2FSK` & `4FSK`
- Some CLI Scripts to generate the shell of a modulation would be great
- Perhaps some better support for 
- Would be great to Dockerize this work for improved ease of use.
