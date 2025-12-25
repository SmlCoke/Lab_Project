*****************************************************
* Lab4 - Task 1: Full Adder Delay Measurement
* Pattern: A -> Cout
* Static inputs: B=0, Cin=1
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

* Sub circuit: 16T Full Adder
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
.ends

* Sub circuit: Buffer
.subckt buffer in out vdd gnd size=1 Lg=20n
Xinv1 in mid vdd gnd INV size='size' Lg='Lg'
Xinv2 mid out vdd gnd INV size='size' Lg='Lg'
.ends

* Source
Vdd VDD GND DC 'SUPPLY'
Vdd_2 VDD2 GND DC 'SUPPLY'
VA Ain GND PULSE (0 'SUPPLY' 500p 50p 50p 950p 2n)
VB Bin GND DC 0
VCI CIin GND DC 'SUPPLY'

* Circuit: Testbench for FA16 Full Adder
XFA16 A B Cin Cout Sum VDD GND FA16 Lg='Lg'
XbufferA Ain A VDD2 GND buffer size = '1' Lg = 'Lg'
XbufferB Bin B VDD2 GND buffer size = '1' Lg = 'Lg'
XbufferCin CIin Cin VDD2 GND buffer size = '1' Lg = 'Lg'
Xsum_load Sum Sum_out VDD2 GND INV size = '2' Lg = 'Lg'
Xcout_load Cout Cout_out VDD2 GND INV size = '2' Lg = 'Lg'

.tran 1p 5n
.probe V(*) I(*)
.measure tran tpLH TRIG V(A) VAL='0.5*SUPPLY' RISE=2 TARG V(Cout) VAL='0.5*SUPPLY' RISE=2
.measure tran tpHL TRIG V(A) VAL='0.5*SUPPLY' FALL=2 TARG V(Cout) VAL='0.5*SUPPLY' FALL=2
.measure tran tp PARAM='(tpLH+tpHL)/2'
.end
