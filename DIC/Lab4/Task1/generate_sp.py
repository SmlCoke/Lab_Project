#!/usr/bin/env python3
"""
Generate HSPICE testbench files for delay measurement of Full Adder circuits.

This script generates .sp files for different input transition patterns to measure
propagation delays (tpLH and tpHL) for both FA16 and FA28 full adder implementations.

Delay patterns to test:
- A->Sum delay (B=0, Cin=0; B=1, Cin=0; B=0, Cin=1; B=1, Cin=1)
- B->Sum delay (A=0, Cin=0; A=1, Cin=0; A=0, Cin=1; A=1, Cin=1)
- Cin->Sum delay (A=0, B=0; A=1, B=0; A=0, B=1; A=1, B=1)
- A->Cout delay (B=0, Cin=0; B=1, Cin=0; B=0, Cin=1; B=1, Cin=1)
- B->Cout delay (A=0, Cin=0; A=1, Cin=0; A=0, Cin=1; A=1, Cin=1)
- Cin->Cout delay (A=0, B=0; A=1, B=0; A=0, B=1; A=1, B=1)
"""

import argparse
from pathlib import Path

# SPICE template for delay measurement
TEMPLATE_DELAY = """*****************************************************
* Lab4 - Task 1: Full Adder Delay Measurement
* Pattern: {input_signal} -> {output_signal}
* Static inputs: {static_desc}
*****************************************************
* global configuration
.option post=2 RUNLVL = 6
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n 


* lib
.include '../../../16nfet.pm'
.include '../../../16pfet.pm'

* We believe that the bulk of all PMOS transistors should be connected to VDD, and the bulk of all NMOS transistors should be connected to GND.

* Sub circuit: INVerter definition
.subckt INV in out vdd gnd size=1 Lg=20n
Mn out in gnd gnd nfet L='Lg' NFIN ='size'
Mp out in vdd vdd pfet L='Lg' NFIN ='size'
.ends INV

{subckt_def}

* Sub circuit: Buffer
.subckt buffer in out vdd gnd size=1 Lg=20n
Xinv1 in mid vdd gnd INV size='size' Lg='Lg'
Xinv2 mid out vdd gnd INV size='size' Lg='Lg'
.ends

* Source
Vdd VDD GND DC 'SUPPLY'
Vdd_2 VDD2 GND DC 'SUPPLY'
{voltage_sources}

* Circuit: Testbench for {fa_type} Full Adder
X{fa_type} A B Cin Cout Sum VDD GND {fa_type} Lg='Lg'
XbufferA Ain A VDD2 GND buffer size = '1' Lg = 'Lg'
XbufferB Bin B VDD2 GND buffer size = '1' Lg = 'Lg'
XbufferCin CIin Cin VDD2 GND buffer size = '1' Lg = 'Lg'
Xsum_load Sum Sum_out VDD2 GND INV size = '2' Lg = 'Lg'
Xcout_load Cout Cout_out VDD2 GND INV size = '2' Lg = 'Lg'

.tran 1p 10n
.probe V(*) I(*)
{measure_statements}
.end
"""

# FA16 subcircuit definition
FA16_SUBCKT = """* Sub circuit: 16T Full Adder
.subckt FA16 A B Cin Cout Sum vdd gnd Lg=20n
* Cout = (AB' + A'B)Cin + (AB + A'B')A
* Sum = A ⊕ B ⊕ Cin
* Module1 : get AB' + A'B and AB + A'B'
Xinv_B B B_bar vdd gnd INV size = '1' Lg = 'Lg'
Mp2 A B AxorB vdd pfet L='Lg' NFIN='1'
Mn2 A B_bar AxorB gnd nfet L='Lg' NFIN='1'
Mn1 B_bar A AxorB gnd nfet L='Lg' NFIN='1'
Mp1 B A AxorB vdd pfet L='Lg' NFIN='1'
Xinv_AxorB AxorB AxnorB vdd gnd INV size = '1' Lg = 'Lg'
* Module2 : get Sum
Mp4 Cin AxorB Sum vdd pfet L='Lg' NFIN='1'
Mn4 Cin AxnorB Sum gnd nfet L='Lg' NFIN='1'
Mn3 AxnorB Cin Sum gnd nfet L='Lg' NFIN='1'
Mp3 AxorB Cin Sum vdd pfet L='Lg' NFIN='1'
* Module3 : get Cout
Mp6 Cin AxnorB Cout vdd pfet L='Lg' NFIN='1'
Mn6 Cin AxorB Cout gnd nfet L='Lg' NFIN='1'
Mp5 A AxorB Cout vdd pfet L='Lg' NFIN='1'
Mn5 A AxnorB Cout gnd nfet L='Lg' NFIN='1'
.ends"""

# FA28 subcircuit definition
FA28_SUBCKT = """* Sub circuit: 28T Full Adder
.subckt FA28 A B Cin Cout Sum vdd gnd Lg=20n
* Carry-block 
* Cout = AB + (A+B)Cin
* PDN:
Mn1 Cout_bar Cin mn1_source gnd nfet L='Lg' NFIN='1'
Mn2 mn1_source A gnd gnd nfet L='Lg' NFIN='1'
Mn3 mn1_source B gnd gnd nfet L='Lg' NFIN='1'
Mn4 Cout_bar A mn4_source gnd nfet L='Lg' NFIN='1'
Mn5 mn4_source B gnd gnd nfet L='Lg' NFIN='1'
* PUN:
Mp1 Cout_bar Cin mp1_source vdd pfet L='Lg' NFIN='1'
Mp2 mp1_source A vdd vdd pfet L='Lg' NFIN='1'
Mp3 mp1_source B vdd vdd pfet L='Lg' NFIN='1'
Mp4 Cout_bar A mp4_source vdd pfet L='Lg' NFIN='1'
Mp5 mp4_source B vdd vdd pfet L='Lg' NFIN='1'
* Inverter to get Cout
Xinv_cout Cout_bar Cout vdd gnd INV size = '1' Lg = 'Lg'

* Sum-block
* Sum = ABCin + Cout_bar(A + B + Cin)
* PDN:
Mn6 Sum_bar Cout_bar mn6_source gnd nfet L='Lg' NFIN='1'
Mn7 mn6_source A gnd gnd nfet L='Lg' NFIN='1'
Mn8 mn6_source B gnd gnd nfet L='Lg' NFIN='1'
Mn9 mn6_source Cin gnd gnd nfet L='Lg' NFIN='1'
Mn10 Sum_bar Cin mn10_source gnd nfet L='Lg' NFIN='1'
Mn11 mn10_source A Mn11_source gnd nfet L='Lg' NFIN='1'
Mn12 Mn11_source B gnd gnd nfet L='Lg' NFIN='1'
* PUN:
Mp6 Sum_bar Cout_bar mp6_source vdd pfet L='Lg' NFIN='1'
Mp7 mp6_source A vdd vdd pfet L='Lg' NFIN='1'
Mp8 mp6_source B vdd vdd pfet L='Lg' NFIN='1'
Mp9 mp6_source Cin vdd vdd pfet L='Lg' NFIN='1'
Mp10 Sum_bar Cin mp10_source vdd pfet L='Lg' NFIN='1'
Mp11 mp10_source A mp11_source vdd pfet L='Lg' NFIN='1'
Mp12 mp11_source B vdd vdd pfet L='Lg' NFIN='1'
* Inverter to get Sum
Xinv_sum Sum_bar Sum vdd gnd INV size = '1' Lg = 'Lg'
.ends"""


def generate_voltage_sources(input_signal, static_values):
    """
    Generate voltage source definitions for the testbench.
    
    Args:
        input_signal: The signal that transitions ('A', 'B', or 'Cin')
        static_values: Dict with static values for the other two inputs
    
    Returns:
        String containing voltage source definitions
    """
    sources = []
    
    # Create the pulse source for the input signal
    # PULSE format: (V1 V2 TD TR TF PW PER)
    # Transition from 0 to SUPPLY at 2ns, with rise/fall time of 100ps
    if input_signal == 'A':
        sources.append("VA Ain GND PULSE (0 'SUPPLY' 2n 100p 100p 6n 16n)")
    else:
        val = "'SUPPLY'" if static_values.get('A', 0) == 1 else "0"
        sources.append(f"VA Ain GND DC {val}")
    
    if input_signal == 'B':
        sources.append("VB Bin GND PULSE (0 'SUPPLY' 2n 100p 100p 6n 16n)")
    else:
        val = "'SUPPLY'" if static_values.get('B', 0) == 1 else "0"
        sources.append(f"VB Bin GND DC {val}")
    
    if input_signal == 'Cin':
        sources.append("VCI CIin GND PULSE (0 'SUPPLY' 2n 100p 100p 6n 16n)")
    else:
        val = "'SUPPLY'" if static_values.get('Cin', 0) == 1 else "0"
        sources.append(f"VCI CIin GND DC {val}")
    
    return '\n'.join(sources)


def generate_measure_statements(input_signal, output_signal):
    """
    Generate .measure statements for delay measurement.
    
    Args:
        input_signal: The input signal that triggers the measurement
        output_signal: The output signal being measured (Sum or Cout)
    
    Returns:
        String containing .measure statements
    """
    measures = []
    
    # Map input signal names to actual signal names in the netlist
    input_map = {'A': 'A', 'B': 'B', 'Cin': 'Cin'}
    input_node = input_map[input_signal]
    
    # Measure propagation delay low-to-high (tpLH): input rises, output rises
    measures.append(
        f".measure tran tpLH TRIG V({input_node}) VAL='0.5*SUPPLY' RISE=1 "
        f"TARG V({output_signal}) VAL='0.5*SUPPLY' RISE=1"
    )
    
    # Measure propagation delay high-to-low (tpHL): input falls, output falls
    measures.append(
        f".measure tran tpHL TRIG V({input_node}) VAL='0.5*SUPPLY' FALL=1 "
        f"TARG V({output_signal}) VAL='0.5*SUPPLY' FALL=1"
    )
    
    # Calculate average propagation delay
    measures.append(".measure tran tp PARAM='(tpLH+tpHL)/2'")
    
    return '\n'.join(measures)


def generate_delay_testbench(fa_type, input_signal, output_signal, static_values, output_dir):
    """
    Generate a single delay measurement testbench file.
    
    Args:
        fa_type: 'FA16' or 'FA28'
        input_signal: Input that transitions ('A', 'B', or 'Cin')
        output_signal: Output being measured ('Sum' or 'Cout')
        static_values: Dict with values for the other two inputs
        output_dir: Directory to save the .sp file
    """
    # Create static description for the filename and comments
    static_parts = []
    for sig in ['A', 'B', 'Cin']:
        if sig != input_signal:
            static_parts.append(f"{sig}={static_values[sig]}")
    static_desc = ', '.join(static_parts)
    
    # Select appropriate subcircuit definition
    subckt_def = FA16_SUBCKT if fa_type == 'FA16' else FA28_SUBCKT
    
    # Generate voltage sources
    voltage_sources = generate_voltage_sources(input_signal, static_values)
    
    # Generate measure statements
    measure_statements = generate_measure_statements(input_signal, output_signal)
    
    # Fill in the template
    content = TEMPLATE_DELAY.format(
        input_signal=input_signal,
        output_signal=output_signal,
        static_desc=static_desc,
        fa_type=fa_type,
        subckt_def=subckt_def,
        voltage_sources=voltage_sources,
        measure_statements=measure_statements
    )
    
    # Create filename
    filename = f"{fa_type}_delay_{input_signal}_to_{output_signal}_"
    for sig in ['A', 'B', 'Cin']:
        if sig != input_signal:
            filename += f"{sig}{static_values[sig]}_"
    filename = filename.rstrip('_') + '.sp'
    
    # Save file
    output_path = Path(output_dir) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding='utf-8')
    print(f"Generated: {output_path}")


def generate_all_delay_testbenches(fa_type, output_dir):
    """
    Generate all delay measurement testbenches for a given FA type.
    
    Args:
        fa_type: 'FA16' or 'FA28'
        output_dir: Base output directory
    """
    # Define all test patterns
    # For each input->output path, test all combinations of the other two inputs
    
    patterns = []
    
    # A -> Sum delay (vary B and Cin)
    for b in [0, 1]:
        for cin in [0, 1]:
            patterns.append({
                'input': 'A',
                'output': 'Sum',
                'static': {'B': b, 'Cin': cin}
            })
    
    # B -> Sum delay (vary A and Cin)
    for a in [0, 1]:
        for cin in [0, 1]:
            patterns.append({
                'input': 'B',
                'output': 'Sum',
                'static': {'A': a, 'Cin': cin}
            })
    
    # Cin -> Sum delay (vary A and B)
    for a in [0, 1]:
        for b in [0, 1]:
            patterns.append({
                'input': 'Cin',
                'output': 'Sum',
                'static': {'A': a, 'B': b}
            })
    
    # A -> Cout delay (vary B and Cin)
    for b in [0, 1]:
        for cin in [0, 1]:
            patterns.append({
                'input': 'A',
                'output': 'Cout',
                'static': {'B': b, 'Cin': cin}
            })
    
    # B -> Cout delay (vary A and Cin)
    for a in [0, 1]:
        for cin in [0, 1]:
            patterns.append({
                'input': 'B',
                'output': 'Cout',
                'static': {'A': a, 'Cin': cin}
            })
    
    # Cin -> Cout delay (vary A and B)
    for a in [0, 1]:
        for b in [0, 1]:
            patterns.append({
                'input': 'Cin',
                'output': 'Cout',
                'static': {'A': a, 'B': b}
            })
    
    # Generate testbenches for all patterns
    for pattern in patterns:
        generate_delay_testbench(
            fa_type=fa_type,
            input_signal=pattern['input'],
            output_signal=pattern['output'],
            static_values=pattern['static'],
            output_dir=output_dir
        )
    
    print(f"\nGenerated {len(patterns)} testbenches for {fa_type} in {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate HSPICE delay measurement testbenches for Full Adder circuits.'
    )
    parser.add_argument(
        '--fa-type',
        choices=['FA16', 'FA28', 'both'],
        default='both',
        help='Full adder type to generate testbenches for (default: both)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='.',
        help='Output directory for generated files (default: current directory)'
    )
    
    args = parser.parse_args()
    
    base_dir = Path(args.output_dir)
    
    if args.fa_type in ['FA16', 'both']:
        fa16_dir = base_dir / 'FA16' / 'delay'
        generate_all_delay_testbenches('FA16', fa16_dir)
    
    if args.fa_type in ['FA28', 'both']:
        fa28_dir = base_dir / 'FA28' / 'delay'
        generate_all_delay_testbenches('FA28', fa28_dir)
    
    print("\nAll testbenches generated successfully!")


if __name__ == '__main__':
    main()
