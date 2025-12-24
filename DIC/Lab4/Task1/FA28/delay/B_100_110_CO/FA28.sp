*****************************************************
* Lab4 - Task 1: Full Adder Delay Measurement
* Pattern: B -> Cout
* Static inputs: A=1, Cin=0
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

* Sub circuit: 28T Full Adder
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
.ends

* Sub circuit: Buffer
.subckt buffer in out vdd gnd size=1 Lg=20n
Xinv1 in mid vdd gnd INV size='size' Lg='Lg'
Xinv2 mid out vdd gnd INV size='size' Lg='Lg'
.ends

* Source
Vdd VDD GND DC 'SUPPLY'
Vdd_2 VDD2 GND DC 'SUPPLY'
VA Ain GND DC 'SUPPLY'
VB Bin GND PULSE (0 'SUPPLY' 2n 100p 100p 6n 16n)
VCI CIin GND DC 0

* Circuit: Testbench for FA28 Full Adder
XFA28 A B Cin Cout Sum VDD GND FA28 Lg='Lg'
XbufferA Ain A VDD2 GND buffer size = '1' Lg = 'Lg'
XbufferB Bin B VDD2 GND buffer size = '1' Lg = 'Lg'
XbufferCin CIin Cin VDD2 GND buffer size = '1' Lg = 'Lg'
Xsum_load Sum Sum_out VDD2 GND INV size = '2' Lg = 'Lg'
Xcout_load Cout Cout_out VDD2 GND INV size = '2' Lg = 'Lg'

.tran 1p 10n
.probe V(*) I(*)
.measure tran tpLH TRIG V(B) VAL='0.5*SUPPLY' RISE=1 TARG V(Cout) VAL='0.5*SUPPLY' RISE=1
.measure tran tpHL TRIG V(B) VAL='0.5*SUPPLY' FALL=1 TARG V(Cout) VAL='0.5*SUPPLY' FALL=1
.measure tran tp PARAM='(tpLH+tpHL)/2'
.end
